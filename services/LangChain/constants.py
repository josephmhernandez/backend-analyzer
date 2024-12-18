
# # NOT IN USE.

# # AI Model Constants
# CODE_FILE_EXTENSIONS = {
#     ".c", ".cpp", ".cc", ".cxx", ".cs", ".java", ".class", ".jar", ".kt", ".m",
#     ".mm", ".swift", ".go", ".py", ".pyc", ".rb", ".rs", ".scala", ".sh", ".bash",
#     ".zsh", ".bat", ".ps1", ".lua", ".pl", ".pm", ".tcl", ".vbs", ".groovy", ".r",
#     ".jl", ".ex", ".exs", ".erl", ".hrl", ".ml", ".nim", ".cr", ".d", ".clj", ".cljs",
#     ".cljc", ".coffee", ".rkt", ".html", ".htm", ".css", ".js", ".jsx", ".ts", ".tsx",
#     ".json", ".xml", ".php", ".asp", ".aspx", ".jsp", ".erb", ".ejs", ".vue", ".svelte",
#     ".twig", ".liquid", ".md", ".rst", ".tex", ".latex", ".adoc", ".org", ".ipynb", ".sas",
#     ".stata", ".do", ".m", ".mlx", ".sql", ".psql", ".db", ".accdb", ".dbf", ".dat", ".mongo",
#     ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env", ".gradle", ".pom", ".make", ".mk",
#     ".cmake", ".dockerfile", ".vagrantfile", ".jenkinsfile", ".circleci", ".v", ".vh", ".sv",
#     ".vhd", ".vhdl", ".asm", ".s", ".ino", ".mjs", ".cjs", ".es6", ".pde", ".sc", ".as",
#     ".au3", ".applescript", ".wsf", ".rpy", ".ahk", ".txt"
# }

# PACKAGE_FILES = {
#     "package.json",  # Node.js (JavaScript, TypeScript)
#     "yarn.lock",  # Yarn (JavaScript, TypeScript)
#     "pnpm-lock.yaml",  # PNPM (JavaScript, TypeScript)
#     "Pipfile",  # pipenv (Python)
#     "requirements.txt",  # pip (Python)
#     "setup.py",  # setuptools (Python)
#     "pyproject.toml",  # PEP 518 (Python)
#     "environment.yml",  # conda (Python)
#     "Gemfile",  # Bundler (Ruby)
#     "Rakefile",  # Rake (Ruby)
#     "build.gradle",  # Gradle (Java, Groovy, Kotlin)
#     "build.gradle.kts",  # Gradle Kotlin DSL (Java, Groovy, Kotlin)
#     "pom.xml",  # Maven (Java, Scala, Kotlin)
#     "settings.gradle",  # Gradle settings (Java, Groovy, Kotlin)
#     "settings.gradle.kts",  # Gradle Kotlin settings (Java, Groovy, Kotlin)
#     "Cargo.toml",  # Cargo (Rust)
#     "Makefile",  # Make (C, C++, various)
#     "CMakeLists.txt",  # CMake (C, C++)
#     "go.mod",  # Go modules (Go)
#     "Gopkg.toml",  # Dep (Go)
#     "composer.json",  # Composer (PHP)
#     "Carthage",  # Carthage (iOS, Swift, Objective-C)
#     "Podfile",  # CocoaPods (iOS, Swift, Objective-C)
#     "SConstruct",  # SCons (Python-based build system)
#     "SConscript",  # SCons subsidiary script (Python-based build system)
#     "spack.yaml",  # Spack (HPC, scientific computing)
#     "conanfile.txt",  # Conan (C, C++)
#     "conanfile.py",  # Conan (C, C++)
#     "Vagrantfile",  # Vagrant (Virtualization, provisioning)
#     "Dockerfile",  # Docker (Containerization)
#     "docker-compose.yml",  # Docker Compose (Container orchestration)
#     "build.sbt",  # SBT (Scala, Java)
#     "mix.exs",  # Mix (Elixir)
#     "rebar.config",  # Rebar (Erlang)
#     "nimble.json",  # Nimble (Nim)
#     "shard.yml",  # Shards (Crystal)
#     "project.clj",  # Leiningen (Clojure)
#     "deps.edn",  # Clojure CLI/Tools (Clojure)
#     "stack.yaml",  # Stack (Haskell)
#     "cabal.project",  # Cabal (Haskell)
#     "Package.swift",  # Swift Package Manager (Swift)
#     "Chart.yaml",  # Helm (Kubernetes)
#     "requirements.yaml",  # Helm dependencies (Kubernetes)
#     "Brewfile",  # Homebrew (macOS, Linux package management)
#     "PKGBUILD",  # Arch Linux package build script
#     "APKBUILD",  # Alpine Linux package build script
#     "DEBIAN/control",  # Debian package control file
#     "DEBIAN/rules",  # Debian package build rules
#     "metadata.rb",  # Chef Cookbook metadata (Infrastructure as code)
#     "Berksfile",  # Berkshelf (Chef dependency management)
#     "Cheffile",  # Librarian-Chef (Chef dependency management)
#     "Puppetfile",  # Puppet environment (Infrastructure as code)
#     "Manifest.txt",  # Java (JAR manifest)
#     "tox.ini",  # Tox (Python testing)
#     "bower.json",  # Bower (JavaScript, front-end)
#     "elm-package.json",  # Elm package management (Elm)
#     "pubspec.yaml",  # Dart package management (Dart, Flutter)
#     "project.json",  # .NET Core project file (C#, F#, VB.NET)
#     "*.csproj",  # Visual Studio project file (C#, .NET)
#     "*.fsproj",  # Visual Studio project file (F#, .NET)
#     "*.vbproj",  # Visual Studio project file (VB.NET)
#     "*.vcxproj",  # Visual Studio C++ project file
#     "*.sln",  # Visual Studio solution file (Various languages, .NET)
#     "*.uproject",  # Unreal Engine project file (Game development)
#     # Unreal Engine project directory settings (Game development)
#     "*.uprojectdirs",
#     "qmake.pro",  # QMake project file (C++, Qt)
#     "rules_docker",  # Bazel build rules for Docker (Build system)
#     "WORKSPACE",  # Bazel (Build system)
#     "BUILD",  # Bazel build script (Build system)
#     "BUILD.bazel",  # Bazel alternative build script (Build system)
#     "build.zig",  # Zig build script (Zig language)
#     "*.dsp", "*.dsw",  # Visual Studio project/workspace files (Older versions)
#     "GNUmakefile",  # Alternative name for Makefile (GNU Make)
#     "Kconfig",  # Linux Kernel configuration file
#     "*.mk",  # Makefile extension (Make)
#     ".merlin",  # Merlin configuration for OCaml
#     "jbuild",  # Dune (formerly Jbuilder) build system (OCaml)
#     "Jenkinsfile",  # Jenkins CI pipeline configuration
#     "*.proj",  # Generic project file (Common in various languages)
#     "*.pro",  # QMake project file (C++, Qt)
#     "*.sb2", "*.sb3",  # Scratch project files (Educational, Scratch)
#     "*.sas7bdat",  # SAS dataset (SAS)
#     "*.tsproj",  # TypeScript project file (TypeScript)
#     "*.xcodeproj",  # Xcode project file (iOS, macOS development)
#     "*.xcworkspace",  # Xcode workspace file (iOS, macOS development)
#     "*.cbp",  # Code::Blocks project file (C/C++)
#     "*.dev",  # Dev-C++ project file (C/C++)
#     "*.mkd",  # Makefile build description (Various languages)
#     "*.uvprojx",  # Keil uVision project file (Embedded development)
#     "*.uvoptx"  # Keil uVision options file (Embedded development)
# }
