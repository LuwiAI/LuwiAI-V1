
# 🤝 Contributing to LuwiAI-V1

We welcome contributions to LuwiAI-V1! This project is ambitious, combining low-level optimization (Assembly/C) with modern system programming (Rust). Your help is greatly appreciated, whether it's fixing bugs, improving documentation, or optimizing a core kernel.

Please read this document carefully before submitting your contributions.

## ❓ How to Contribute

### 1. Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](LINK_TO_CODE_OF_CONDUCT_IF_AVAILABLE).

### 2. Reporting Bugs and Issues

If you find a bug, please use the dedicated template:

* **[🐛 Bug Report Template]**

### 3. Suggesting Features and Enhancements

If you have an idea for a new feature, performance optimization, or architectural improvement:

* **[✨ Feature Request Template]**

### 4. Code Contribution Workflow

1.  **Fork** the repository and clone your fork.
2.  Create a descriptive branch (e.g., `feat/avx512-gemm-kernel`, `fix/rust-tokenizer-bug`).
3.  Implement your changes.
4.  Write comprehensive tests that cover the new feature or bug fix.
5.  Ensure all existing tests pass on **both** target architectures (x86-64 and ARM64).
6.  Ensure your code adheres to the style guides (see section below).
7.  Commit your changes using a descriptive, Conventional Commit message (see section below).
8.  Push your branch to your fork.
9.  Open a Pull Request (PR) against the `develop` branch of the main repository, filling out the **[Pull Request Template]** completely.

## 🛠 Development Setup

Due to the multi-language nature of LuwiAI-V1, setting up the environment is crucial.

### Prerequisites

You must have the following tools installed:

* **Git**
* **Rust Toolchain:** Stable version (required for high-level logic and FFI bindings).
* **C/C++ Compiler:** GCC or Clang (required for the runtime engine).
* **CMake:** Version 3.15 or higher (required for build system).
* **NASM:** Netwide Assembler (required for Assembly kernels).
* **Python:** Version 3.9+ (required for `tools/` and utilities).

### Building the Project

The core runtime is managed by CMake:

```bash
# 1. Build for Native Architecture (e.g., x86-64)
mkdir build_native
cd build_native
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j

# 2. Build Rust components
# Navigate to the relevant Rust directory (e.g., code/src/rust/cli)
cargo build --release
````

### Testing

Please run all tests before submitting a PR.

  * **C/C++ Tests:** Executables are found in the `build_native/tests/unit/` directory.
  * **Rust Tests:** Run via Cargo: `cargo test --all`.

## 📜 Coding Style and Standards

### 1\. Commit Messages (Conventional Commits)

We use **Conventional Commits** for clear history tracking. Each commit message must start with a type:

| Type | Description | Example |
| :--- | :--- | :--- |
| `feat` | New feature or functionality | `feat: Add Top-P sampling to decoder` |
| `fix` | Bug fix | `fix: Correct memory alignment bug in f16 GEMM` |
| `perf` | Code change that improves performance | `perf: Optimize LayerNorm using AVX-512` |
| `docs` | Documentation only changes | `docs: Update CONTRIBUTING.md` |
| `chore` | Routine tasks, build process changes, dependency updates | `chore: Update Rust dependencies` |
| `refactor`| Refactoring code, no functional changes | `refactor: Rename luwi_core.h functions` |
| `test` | Adding or correcting tests | `test: Add unit test for ReLU activation` |

### 2\. Language-Specific Guidelines

  * **Rust:** Follow the standard idiomatic Rust practices and use `cargo fmt`.
  * **C/C++:** Use clear variable names. Prioritize thread safety in the runtime. When writing wrappers for Assembly, use `extern "C"` where appropriate.
  * **Assembly (NASM):** Code must be heavily commented, explaining register usage, memory access patterns, and the specific SIMD instructions (e.g., AVX, NEON) being utilized. Performance gains must be validated with benchmarks.

Thank you for helping us make LuwiAI-V1 a robust and high-performance small language model\!
