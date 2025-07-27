# Dependency Mappings

## Overview
This data file contains comprehensive mappings between generic dependency names and platform-specific package names, installation commands, and verification methods. These mappings enable I.S.A.A.C. to generate accurate cross-platform installation scripts.

## Runtime Dependencies

### Node.js Runtime
```json
{
  "nodejs": {
    "generic_name": "nodejs",
    "description": "Node.js JavaScript runtime",
    "category": "runtime",
    "platforms": {
      "windows": {
        "chocolatey": {
          "package_name": "nodejs",
          "install_command": "choco install nodejs -y",
          "verify_command": "node --version",
          "uninstall_command": "choco uninstall nodejs -y"
        },
        "winget": {
          "package_name": "OpenJS.NodeJS",
          "install_command": "winget install OpenJS.NodeJS",
          "verify_command": "node --version",
          "uninstall_command": "winget uninstall OpenJS.NodeJS"
        },
        "manual": {
          "download_url": "https://nodejs.org/dist/v{version}/node-v{version}-x64.msi",
          "install_command": "msiexec /i node-v{version}-x64.msi /quiet",
          "verify_command": "node --version"
        }
      },
      "linux": {
        "ubuntu": {
          "package_name": "nodejs npm",
          "install_command": "sudo apt-get update && sudo apt-get install -y nodejs npm",
          "verify_command": "node --version && npm --version",
          "uninstall_command": "sudo apt-get remove -y nodejs npm"
        },
        "centos": {
          "package_name": "nodejs npm",
          "install_command": "sudo yum install -y nodejs npm",
          "verify_command": "node --version && npm --version",
          "uninstall_command": "sudo yum remove -y nodejs npm"
        },
        "fedora": {
          "package_name": "nodejs npm",
          "install_command": "sudo dnf install -y nodejs npm",
          "verify_command": "node --version && npm --version",
          "uninstall_command": "sudo dnf remove -y nodejs npm"
        },
        "arch": {
          "package_name": "nodejs npm",
          "install_command": "sudo pacman -S nodejs npm",
          "verify_command": "node --version && npm --version",
          "uninstall_command": "sudo pacman -R nodejs npm"
        }
      },
      "macos": {
        "homebrew": {
          "package_name": "node",
          "install_command": "brew install node",
          "verify_command": "node --version && npm --version",
          "uninstall_command": "brew uninstall node"
        },
        "macports": {
          "package_name": "nodejs18",
          "install_command": "sudo port install nodejs18",
          "verify_command": "node --version",
          "uninstall_command": "sudo port uninstall nodejs18"
        }
      }
    },
    "version_constraints": {
      "minimum": "14.0.0",
      "recommended": "18.0.0",
      "maximum": "20.x.x"
    }
  }
}
```

### Python Runtime
```json
{
  "python": {
    "generic_name": "python",
    "description": "Python programming language runtime",
    "category": "runtime",
    "platforms": {
      "windows": {
        "chocolatey": {
          "package_name": "python",
          "install_command": "choco install python -y",
          "verify_command": "python --version",
          "uninstall_command": "choco uninstall python -y"
        },
        "winget": {
          "package_name": "Python.Python.3",
          "install_command": "winget install Python.Python.3",
          "verify_command": "python --version",
          "uninstall_command": "winget uninstall Python.Python.3"
        },
        "manual": {
          "download_url": "https://www.python.org/ftp/python/{version}/python-{version}-amd64.exe",
          "install_command": "python-{version}-amd64.exe /quiet InstallAllUsers=1 PrependPath=1",
          "verify_command": "python --version"
        }
      },
      "linux": {
        "ubuntu": {
          "package_name": "python3 python3-pip",
          "install_command": "sudo apt-get update && sudo apt-get install -y python3 python3-pip",
          "verify_command": "python3 --version && pip3 --version",
          "uninstall_command": "sudo apt-get remove -y python3 python3-pip"
        },
        "centos": {
          "package_name": "python3 python3-pip",
          "install_command": "sudo yum install -y python3 python3-pip",
          "verify_command": "python3 --version && pip3 --version",
          "uninstall_command": "sudo yum remove -y python3 python3-pip"
        },
        "fedora": {
          "package_name": "python3 python3-pip",
          "install_command": "sudo dnf install -y python3 python3-pip",
          "verify_command": "python3 --version && pip3 --version",
          "uninstall_command": "sudo dnf remove -y python3 python3-pip"
        }
      },
      "macos": {
        "homebrew": {
          "package_name": "python@3.11",
          "install_command": "brew install python@3.11",
          "verify_command": "python3 --version && pip3 --version",
          "uninstall_command": "brew uninstall python@3.11"
        }
      }
    },
    "version_constraints": {
      "minimum": "3.8.0",
      "recommended": "3.11.0",
      "maximum": "3.12.x"
    }
  }
}
```

### Java Runtime
```json
{
  "java": {
    "generic_name": "java",
    "description": "Java Runtime Environment",
    "category": "runtime",
    "platforms": {
      "windows": {
        "chocolatey": {
          "package_name": "openjdk",
          "install_command": "choco install openjdk -y",
          "verify_command": "java -version",
          "uninstall_command": "choco uninstall openjdk -y"
        },
        "winget": {
          "package_name": "EclipseAdoptium.Temurin.17.JDK",
          "install_command": "winget install EclipseAdoptium.Temurin.17.JDK",
          "verify_command": "java -version",
          "uninstall_command": "winget uninstall EclipseAdoptium.Temurin.17.JDK"
        }
      },
      "linux": {
        "ubuntu": {
          "package_name": "openjdk-17-jdk",
          "install_command": "sudo apt-get update && sudo apt-get install -y openjdk-17-jdk",
          "verify_command": "java -version && javac -version",
          "uninstall_command": "sudo apt-get remove -y openjdk-17-jdk"
        },
        "centos": {
          "package_name": "java-17-openjdk-devel",
          "install_command": "sudo yum install -y java-17-openjdk-devel",
          "verify_command": "java -version && javac -version",
          "uninstall_command": "sudo yum remove -y java-17-openjdk-devel"
        }
      },
      "macos": {
        "homebrew": {
          "package_name": "openjdk@17",
          "install_command": "brew install openjdk@17",
          "verify_command": "java -version",
          "uninstall_command": "brew uninstall openjdk@17"
        }
      }
    },
    "version_constraints": {
      "minimum": "11",
      "recommended": "17",
      "maximum": "21"
    }
  }
}
```

## Database Systems

### PostgreSQL
```json
{
  "postgresql": {
    "generic_name": "postgresql",
    "description": "PostgreSQL database server",
    "category": "database",
    "platforms": {
      "windows": {
        "chocolatey": {
          "package_name": "postgresql",
          "install_command": "choco install postgresql -y",
          "verify_command": "psql --version",
          "service_name": "postgresql-x64-14",
          "default_port": 5432
        }
      },
      "linux": {
        "ubuntu": {
          "package_name": "postgresql postgresql-contrib",
          "install_command": "sudo apt-get update && sudo apt-get install -y postgresql postgresql-contrib",
          "verify_command": "psql --version",
          "service_name": "postgresql",
          "default_port": 5432,
          "post_install": [
            "sudo systemctl enable postgresql",
            "sudo systemctl start postgresql"
          ]
        },
        "centos": {
          "package_name": "postgresql-server postgresql-contrib",
          "install_command": "sudo yum install -y postgresql-server postgresql-contrib",
          "verify_command": "psql --version",
          "service_name": "postgresql",
          "post_install": [
            "sudo postgresql-setup initdb",
            "sudo systemctl enable postgresql",
            "sudo systemctl start postgresql"
          ]
        }
      },
      "macos": {
        "homebrew": {
          "package_name": "postgresql",
          "install_command": "brew install postgresql",
          "verify_command": "psql --version",
          "service_name": "postgresql",
          "post_install": [
            "brew services start postgresql"
          ]
        }
      }
    },
    "configuration": {
      "data_directory": {
        "windows": "C:\\Program Files\\PostgreSQL\\14\\data",
        "linux": "/var/lib/postgresql/data",
        "macos": "/usr/local/var/postgres"
      },
      "config_file": {
        "windows": "C:\\Program Files\\PostgreSQL\\14\\data\\postgresql.conf",
        "linux": "/etc/postgresql/14/main/postgresql.conf",
        "macos": "/usr/local/var/postgres/postgresql.conf"
      }
    }
  }
}
```

### MySQL
```json
{
  "mysql": {
    "generic_name": "mysql",
    "description": "MySQL database server",
    "category": "database",
    "platforms": {
      "windows": {
        "chocolatey": {
          "package_name": "mysql",
          "install_command": "choco install mysql -y",
          "verify_command": "mysql --version",
          "service_name": "MySQL80"
        }
      },
      "linux": {
        "ubuntu": {
          "package_name": "mysql-server",
          "install_command": "sudo apt-get update && sudo apt-get install -y mysql-server",
          "verify_command": "mysql --version",
          "service_name": "mysql",
          "post_install": [
            "sudo systemctl enable mysql",
            "sudo systemctl start mysql",
            "sudo mysql_secure_installation"
          ]
        },
        "centos": {
          "package_name": "mysql-server",
          "install_command": "sudo yum install -y mysql-server",
          "verify_command": "mysql --version",
          "service_name": "mysqld"
        }
      },
      "macos": {
        "homebrew": {
          "package_name": "mysql",
          "install_command": "brew install mysql",
          "verify_command": "mysql --version",
          "post_install": [
            "brew services start mysql"
          ]
        }
      }
    },
    "default_port": 3306
  }
}
```

## Web Servers

### Nginx
```json
{
  "nginx": {
    "generic_name": "nginx",
    "description": "Nginx web server",
    "category": "web_server",
    "platforms": {
      "windows": {
        "chocolatey": {
          "package_name": "nginx",
          "install_command": "choco install nginx -y",
          "verify_command": "nginx -v",
          "service_name": "nginx"
        }
      },
      "linux": {
        "ubuntu": {
          "package_name": "nginx",
          "install_command": "sudo apt-get update && sudo apt-get install -y nginx",
          "verify_command": "nginx -v",
          "service_name": "nginx",
          "post_install": [
            "sudo systemctl enable nginx",
            "sudo systemctl start nginx"
          ]
        },
        "centos": {
          "package_name": "nginx",
          "install_command": "sudo yum install -y nginx",
          "verify_command": "nginx -v",
          "service_name": "nginx"
        }
      },
      "macos": {
        "homebrew": {
          "package_name": "nginx",
          "install_command": "brew install nginx",
          "verify_command": "nginx -v",
          "post_install": [
            "brew services start nginx"
          ]
        }
      }
    },
    "configuration": {
      "config_file": {
        "windows": "C:\\tools\\nginx\\conf\\nginx.conf",
        "linux": "/etc/nginx/nginx.conf",
        "macos": "/usr/local/etc/nginx/nginx.conf"
      },
      "document_root": {
        "windows": "C:\\tools\\nginx\\html",
        "linux": "/var/www/html",
        "macos": "/usr/local/var/www"
      }
    },
    "default_port": 80
  }
}
```

## Development Tools

### Git
```json
{
  "git": {
    "generic_name": "git",
    "description": "Git version control system",
    "category": "development_tool",
    "platforms": {
      "windows": {
        "chocolatey": {
          "package_name": "git",
          "install_command": "choco install git -y",
          "verify_command": "git --version"
        },
        "winget": {
          "package_name": "Git.Git",
          "install_command": "winget install Git.Git",
          "verify_command": "git --version"
        }
      },
      "linux": {
        "ubuntu": {
          "package_name": "git",
          "install_command": "sudo apt-get update && sudo apt-get install -y git",
          "verify_command": "git --version"
        },
        "centos": {
          "package_name": "git",
          "install_command": "sudo yum install -y git",
          "verify_command": "git --version"
        }
      },
      "macos": {
        "homebrew": {
          "package_name": "git",
          "install_command": "brew install git",
          "verify_command": "git --version"
        },
        "builtin": {
          "verify_command": "git --version",
          "note": "Git is included with Xcode Command Line Tools"
        }
      }
    }
  }
}
```

### Docker
```json
{
  "docker": {
    "generic_name": "docker",
    "description": "Docker containerization platform",
    "category": "containerization",
    "platforms": {
      "windows": {
        "chocolatey": {
          "package_name": "docker-desktop",
          "install_command": "choco install docker-desktop -y",
          "verify_command": "docker --version",
          "requires_restart": true
        },
        "winget": {
          "package_name": "Docker.DockerDesktop",
          "install_command": "winget install Docker.DockerDesktop",
          "verify_command": "docker --version"
        }
      },
      "linux": {
        "ubuntu": {
          "install_script": [
            "sudo apt-get update",
            "sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release",
            "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg",
            "echo \"deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null",
            "sudo apt-get update",
            "sudo apt-get install -y docker-ce docker-ce-cli containerd.io"
          ],
          "verify_command": "docker --version",
          "service_name": "docker",
          "post_install": [
            "sudo systemctl enable docker",
            "sudo systemctl start docker",
            "sudo usermod -aG docker $USER"
          ]
        }
      },
      "macos": {
        "homebrew": {
          "package_name": "docker",
          "install_command": "brew install --cask docker",
          "verify_command": "docker --version"
        }
      }
    }
  }
}
```

## System Utilities

### Curl
```json
{
  "curl": {
    "generic_name": "curl",
    "description": "Command line HTTP client",
    "category": "system_utility",
    "platforms": {
      "windows": {
        "builtin": {
          "verify_command": "curl --version",
          "note": "Available by default in Windows 10 1803+"
        },
        "chocolatey": {
          "package_name": "curl",
          "install_command": "choco install curl -y",
          "verify_command": "curl --version"
        }
      },
      "linux": {
        "ubuntu": {
          "package_name": "curl",
          "install_command": "sudo apt-get update && sudo apt-get install -y curl",
          "verify_command": "curl --version"
        },
        "centos": {
          "package_name": "curl",
          "install_command": "sudo yum install -y curl",
          "verify_command": "curl --version"
        }
      },
      "macos": {
        "builtin": {
          "verify_command": "curl --version",
          "note": "Available by default on macOS"
        }
      }
    }
  }
}
```

## Package Manager Mappings

### Package Manager Availability
```json
{
  "package_managers": {
    "windows": {
      "chocolatey": {
        "install_url": "https://chocolatey.org/install.ps1",
        "install_command": "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))",
        "verify_command": "choco --version"
      },
      "winget": {
        "builtin": true,
        "minimum_windows_version": "10.0.17763",
        "verify_command": "winget --version"
      },
      "scoop": {
        "install_command": "iwr -useb get.scoop.sh | iex",
        "verify_command": "scoop --version"
      }
    },
    "linux": {
      "apt": {
        "distributions": ["ubuntu", "debian"],
        "verify_command": "apt --version"
      },
      "yum": {
        "distributions": ["centos", "rhel"],
        "verify_command": "yum --version"
      },
      "dnf": {
        "distributions": ["fedora"],
        "verify_command": "dnf --version"
      },
      "pacman": {
        "distributions": ["arch", "manjaro"],
        "verify_command": "pacman --version"
      },
      "zypper": {
        "distributions": ["opensuse"],
        "verify_command": "zypper --version"
      }
    },
    "macos": {
      "homebrew": {
        "install_command": "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"",
        "verify_command": "brew --version"
      },
      "macports": {
        "install_url": "https://www.macports.org/install.php",
        "verify_command": "port version"
      }
    }
  }
}
```

## Version Mapping Rules

### Version Resolution
```json
{
  "version_resolution": {
    "semantic_versioning": {
      "pattern": "^(\\d+)\\.(\\d+)\\.(\\d+)(?:-([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?(?:\\+([0-9A-Za-z-]+(?:\\.[0-9A-Za-z-]+)*))?$",
      "comparison_rules": {
        "major": "breaking_changes",
        "minor": "backward_compatible_features",
        "patch": "backward_compatible_fixes"
      }
    },
    "constraint_operators": {
      "^": "compatible_within_major",
      "~": "compatible_within_minor",
      ">=": "greater_than_or_equal",
      "<=": "less_than_or_equal",
      ">": "greater_than",
      "<": "less_than",
      "=": "exact_match"
    },
    "platform_specific_versions": {
      "nodejs": {
        "windows": "latest_lts",
        "linux": "latest_lts",
        "macos": "latest_lts"
      },
      "python": {
        "windows": "3.11.x",
        "linux": "3.11.x",
        "macos": "3.11.x"
      }
    }
  }
}
```
