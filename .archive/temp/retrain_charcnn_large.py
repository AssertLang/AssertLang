#!/usr/bin/env python3
"""
Re-train CharCNN on large dataset (9,760 examples).

Uses training_dataset_large.json instead of training_dataset_full.json
"""

import sys
from pathlib import Path

# Import training module
from ml.train import (
    build_operation_vocab,
    OperationDataset,
    CharCNN,
    OperationEmbedding,
    InfoNCE,
    train_epoch,
    evaluate
)

import torch
import torch.optim as optim
from torch.utils.data import DataLoader
from ml.tokenizer import CharTokenizer
import time


def main():
    print("=" * 80)
    print("CharCNN Re-training - Large Dataset (9,760 examples)")
    print("=" * 80)
    print()

    # Configuration
    data_path = "training_dataset_large.json"
    vocab_size = 128
    max_length = 256
    embed_dim = 64
    hidden_dim = 256
    output_dim = 256
    batch_size = 32
    num_epochs = 20  # Reduced from 50 for faster training with large dataset
    learning_rate = 1e-3
    temperature = 0.07
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    print(f"Device: {device}")
    print(f"Dataset: {data_path}")
    print(f"Batch size: {batch_size}")
    print(f"Epochs: {num_epochs}")
    print(f"Learning rate: {learning_rate}")
    print(f"Temperature: {temperature}")
    print()

    # Check dataset
    if not Path(data_path).exists():
        print(f"ERROR: Dataset not found at {data_path}")
        print("Please run generate_training_dataset_large.py first")
        return 1

    # Build operation vocabulary
    operation_to_id, id_to_operation = build_operation_vocab(data_path)
    num_operations = len(operation_to_id)
    print(f"Operations: {num_operations}")
    print()

    # Create tokenizer
    tokenizer = CharTokenizer(vocab_size=vocab_size, max_length=max_length)

    # Create dataset and dataloader
    dataset = OperationDataset(data_path, tokenizer, operation_to_id)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    print(f"Batches per epoch: {len(dataloader)}")
    print()

    # Create model
    model = CharCNN(
        vocab_size=vocab_size,
        embed_dim=embed_dim,
        hidden_dim=hidden_dim,
        output_dim=output_dim,
        kernel_sizes=[3, 5, 7],
        num_filters=64,
        dropout=0.1
    ).to(device)

    operation_emb = OperationEmbedding(
        num_operations=num_operations,
        embed_dim=output_dim
    ).to(device)

    print(f"Model parameters: {model.count_parameters():,}")
    print()

    # Create loss and optimizer
    loss_fn = InfoNCE(temperature=temperature)
    optimizer = optim.Adam(
        list(model.parameters()) + list(operation_emb.parameters()),
        lr=learning_rate
    )

    # Training loop
    print("=" * 80)
    print("Training")
    print("=" * 80)
    print()

    best_accuracy = 0.0
    start_time = time.time()

    for epoch in range(num_epochs):
        epoch_start = time.time()

        # Train
        train_metrics = train_epoch(model, operation_emb, dataloader, loss_fn, optimizer, device)

        # Evaluate
        eval_metrics = evaluate(model, operation_emb, dataloader, loss_fn, device)

        epoch_time = time.time() - epoch_start

        # Log progress
        print(f"Epoch {epoch+1:2d}/{num_epochs} ({epoch_time:.1f}s) | "
              f"Train Loss: {train_metrics['loss']:.4f} | "
              f"Train Acc: {train_metrics['accuracy']:.2%} | "
              f"Eval Loss: {eval_metrics['loss']:.4f} | "
              f"Eval Acc: {eval_metrics['accuracy']:.2%}")

        # Save best model
        if eval_metrics['accuracy'] > best_accuracy:
            best_accuracy = eval_metrics['accuracy']
            torch.save({
                'epoch': epoch + 1,
                'model_state_dict': model.state_dict(),
                'operation_emb_state_dict': operation_emb.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'accuracy': best_accuracy,
                'operation_to_id': operation_to_id,
                'id_to_operation': id_to_operation,
                'training_size': len(dataset),
            }, 'ml/charcnn_large.pt')

        # Check if we hit 100% accuracy
        if eval_metrics['accuracy'] >= 1.0:
            print()
            print(f"✅ Achieved 100% accuracy at epoch {epoch+1}!")
            break

    total_time = time.time() - start_time

    print()
    print("=" * 80)
    print("Training Complete")
    print("=" * 80)
    print(f"Best accuracy: {best_accuracy:.2%}")
    print(f"Total time: {total_time/60:.1f} minutes")
    print(f"Model saved: ml/charcnn_large.pt")
    print()
    print(f"Training dataset size: {len(dataset):,} examples")
    print(f"Previous dataset size: 193 examples")
    print(f"Improvement: {len(dataset)/193:.1f}x more data")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
