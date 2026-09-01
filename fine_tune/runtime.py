"""Hugging Face + PEFT loop. Imported only when CUDA is actually present."""

from __future__ import annotations

from fine_tune.planner import FineTunePlan


def run_training(plan: FineTunePlan, data: str | None = None) -> int:
    """Run LoRA or full FT.

    Kept behind this module so laptop pytest never pulls torch. The
    implementation is intentionally small: Trainer + optional PEFT, packed
    to ``plan.recipe.context_length`` (5,120).
    """
    try:
        import torch
        from transformers import (
            AutoModelForCausalLM,
            AutoTokenizer,
            Trainer,
            TrainingArguments,
        )
    except ImportError as exc:
        raise RuntimeError(
            "GPU training extras are missing. On the RunPod node the bootstrap "
            "script installs transformers/peft. Locally use --dry-run."
        ) from exc

    recipe = plan.recipe
    tokenizer = AutoTokenizer.from_pretrained(recipe.base_model, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        recipe.base_model,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True,
    )
    if recipe.method == "lora":
        from peft import LoraConfig, TaskType, get_peft_model

        model = get_peft_model(
            model,
            LoraConfig(
                r=recipe.lora_rank,
                lora_alpha=recipe.lora_rank * 2,
                lora_dropout=0.05,
                bias="none",
                task_type=TaskType.CAUSAL_LM,
                target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
            ),
        )

    steps = recipe.smoke_steps if plan.smoke else recipe.max_steps
    dataset = _load_or_smoke_dataset(tokenizer, recipe.context_length, data)

    args = TrainingArguments(
        output_dir=f"/workspace/outputs/{recipe.name}",
        per_device_train_batch_size=recipe.micro_batch_size,
        gradient_accumulation_steps=recipe.grad_accum,
        max_steps=steps,
        learning_rate=recipe.learning_rate,
        bf16=True,
        logging_steps=1,
        save_steps=max(steps, 1),
        report_to=[],
        remove_unused_columns=False,
        dataloader_num_workers=2,
    )
    trainer = Trainer(model=model, args=args, train_dataset=dataset)
    trainer.train()
    trainer.save_model(args.output_dir)
    return 0


def _load_or_smoke_dataset(tokenizer, context_length: int, data: str | None):
    from datasets import Dataset

    if data:
        from datasets import load_dataset

        raw = load_dataset(data, split="train")
        texts = [row["text"] if "text" in row else str(row) for row in raw]
    else:
        # Tiny reasoning-flavored smoke so a pod without a dataset still
        # exercises the loop instead of idling at $X/hour.
        texts = [
            "Q: 17+25?\nA: 17+25=42. The answer is 42.",
            "Q: A train leaves at 3pm and travels 2 hours. When does it arrive?\nA: 5pm.",
            "Q: Write a Python function that returns the sum of a list.\nA: def total(xs):\n    return sum(xs)",
        ] * 64

    def tokenize(batch: dict) -> dict:
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=context_length,
            padding="max_length",
        )

    ds = Dataset.from_dict({"text": texts})
    ds = ds.map(tokenize, batched=True, remove_columns=["text"])
    ds = ds.map(lambda row: {"labels": row["input_ids"]})
    return ds
