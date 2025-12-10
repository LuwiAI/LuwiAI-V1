---
name: Pull Request
about: Propose changes for review and merging into the LuwiAI-V1 codebase.
title: "[TYPE]: Concise description of the change"
labels: 'review-needed'
assignees: ''
---

## 🧐 Purpose of the Pull Request

Please provide a brief description of the goal of this PR. (e.g., Fixes issue #123, Implements new AVX-512 kernel, Adds documentation for the Rust FFI bindings).

## ✅ Checklist

Please check off the following items to ensure your PR is ready for review.

- [ ] I have read and followed the [CONTRIBUTING.md] guidelines.
- [ ] My code follows the project's coding style guidelines (Rust fmt, C/C++ style).
- [ ] My change requires a change to the documentation (README, API docs).
  - [ ] If yes, I have updated the documentation accordingly.
- [ ] I have added tests to cover my changes (unit tests, functional tests).
  - [ ] If yes, all new and existing tests pass successfully.
- [ ] The change has been tested on **both** X86-64 and ARM64 architectures (if applicable to core runtime).

## 🚀 Type of Change

What kind of change does this PR introduce? (Select all that apply)

- [ ] **Feat:** A new feature or enhancement.
- [ ] **Fix:** A bug fix.
- [ ] **Perf:** A code change that improves performance (e.g., new Assembly kernel).
- [ ] **Docs:** Documentation-only changes.
- [ ] **Chore:** Routine tasks, build process changes, dependency updates.
- [ ] **Test:** Adding missing tests or correcting existing tests.
- [ ] **Refactor:** A code change that neither fixes a bug nor adds a feature.

## 🔬 Implementation Details

### Module(s) Affected:

* [ ] `src/assembly/x86_64` (Assembly Kernels)
* [ ] `src/assembly/arm64` (Assembly Kernels)
* [ ] `code/src/c_cpp/runtime` (C/C++ Core Runtime)
* [ ] `code/src/rust/bindings` (FFI Bindings)
* [ ] `code/src/rust/luwi_core` (Rust Core Logic: Tokenizer, Decoder)
* [ ] `tools/` (Training/Scraping/Quantization Scripts)
* [ ] Other: [Please specify]

### Detailed Description of Changes:

Provide technical details on *how* the change was implemented. If this includes a performance optimization (e.g., in Assembly), please provide benchmark results if possible.

## 🖼 Screenshots / Benchmarks (Optional)

If this is a visual change or a performance optimization, include screenshots or benchmark data here.
