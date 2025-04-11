

def get_default_structure(src: str, main: str) -> dict:
    return {
        src: {
            "__init__.py": "",
            main: f"# Arquivo principal: {main}\n"
        },
        "tests": {
            "__init__.py": "",
            f"test_{main.replace('.py', '')}.py": "# Teste inicial\n"
        },
        "projectgen": {
            "__init__.py": "",
            "core": {
                "__init__.py": "",
                "generator.py": "# Lógica de criação\n",
                "templates.py": "# Templates\n",
                "helpers": {
                    "__init__.py": "",
                    "module.py": "# Lógica de criação de módulos\n",
                    "utils.py": "# Funções utilitárias\n"
                }
            }
        }
    }

project_templates = {
    "common_files": [
      "README.md",
      "pyproject.toml",
      "setup.cfg",
      "requirements.txt",
      ".gitignore",
      ".env.example"
    ],
    "project_types": {
      "simple_script": {
        "description": "Projeto com um único script principal e módulos auxiliares.",
        "structure": {
          "my_project/": {
            "__main__.py": "",
            "utils.py": "",
            "config.py": ""
          },
          "tests/": {
            "test_utils.py": ""
          }
        }
      },
      "python_package": {
        "description": "Pacote Python instalável com módulos internos.",
        "structure": {
          "my_package/": {
            "__init__.py": "",
            "core/": {
              "__init__.py": "",
              "module_a.py": "",
              "module_b.py": ""
            },
            "helpers/": {
              "__init__.py": "",
              "tools.py": ""
            }
          },
          "tests/": {
            "__init__.py": "",
            "test_module_a.py": "",
            "test_module_b.py": ""
          }
        }
      },
      "modular_application": {
        "description": "Aplicação modular com múltiplos componentes.",
        "structure": {
          "my_app/": {
            "__init__.py": "",
            "main.py": "",
            "config/": {
              "__init__.py": "",
              "settings.py": ""
            },
            "modules/": {
              "__init__.py": "",
              "mod_base.py": "",
              "mod_example/": {
                "__init__.py": "",
                "logic.py": "",
                "handlers.py": ""
              }
            },
            "services/": {
              "__init__.py": "",
              "database.py": "",
              "api.py": ""
            }
          },
          "tests/": {
            "__init__.py": "",
            "modules/": {
              "__init__.py": "",
              "test_mod_example.py": ""
            },
            "services/": {
              "__init__.py": "",
              "test_database.py": "",
              "test_api.py": ""
            }
          },
          "scripts/": {
            "start_dev.sh": "",
            "setup_env.py": ""
          }
        }
      },
      "fastapi_api": {
        "description": "API criada com FastAPI.",
        "structure": {
          "app/": {
            "__init__.py": "",
            "main.py": "from fastapi import FastAPI\nfrom app.routes import router as api_router\n\napp = FastAPI(title='My FastAPI App')\napp.include_router(api_router)",
            "routes/": {
              "__init__.py": "",
              "example.py": "from fastapi import APIRouter\n\nrouter = APIRouter()\n\n@router.get('/')\ndef read_root():\n    return {'message': 'Hello from FastAPI'}"
            },
            "models/": {
              "__init__.py": "",
              "example_model.py": ""
            },
            "services/": {
              "__init__.py": "",
              "example_service.py": ""
            },
            "config/": {
              "__init__.py": "",
              "settings.py": "import os\n\nDEBUG = os.getenv('DEBUG', 'true') == 'true'"
            }
          },
          "tests/": {
            "test_example.py": ""
          },
          "scripts/": {
            "start.sh": "uvicorn app.main:app --reload"
          }
        }
      },
      "flask_api": {
        "description": "API criada com Flask, incluindo frontend com HTML, CSS e JS.",
        "structure": {
          "app/": {
            "__init__.py": "from flask import Flask\n\ndef create_app():\n    app = Flask(__name__)\n\n    from .routes import main_bp, api_bp\n    app.register_blueprint(main_bp)\n    app.register_blueprint(api_bp, url_prefix='/api')\n\n    return app",
            "routes/": {
              "__init__.py": "from .main import main_bp\nfrom .api import api_bp",
              "main.py": "from flask import Blueprint, render_template\n\nmain_bp = Blueprint('main', __name__)\n\n@main_bp.route('/')\ndef home():\n    return render_template('index.html')",
              "api.py": "from flask import Blueprint, jsonify\n\napi_bp = Blueprint('api', __name__)\n\n@api_bp.route('/ping')\ndef ping():\n    return jsonify({'message': 'pong'})"
            },
            "templates/": {
              "index.html": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <title>My Flask App</title>\n    <link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/style.css') }}\">\n</head>\n<body>\n    <h1>Hello from Flask!</h1>\n    <script src=\"{{ url_for('static', filename='js/script.js') }}\"></script>\n</body>\n</html>"
            },
            "static/": {
              "css/": {
                "style.css": "body {\n    font-family: Arial, sans-serif;\n    background-color: #f9f9f9;\n}"
              },
              "js/": {
                "script.js": "console.log(\"JS loaded correctly!\");"
              }
            },
            "config.py": "import os\n\nDEBUG = os.getenv(\"DEBUG\", \"true\").lower() == \"true\""
          },
          "tests/": {
            "test_main.py": "from app import create_app\n\ndef test_home():\n    app = create_app()\n    client = app.test_client()\n    response = client.get('/')\n    assert response.status_code == 200"
          },
          "run.py": "from app import create_app\n\napp = create_app()\n\nif __name__ == '__main__':\n    app.run(debug=True)",
          "requirements.txt": "flask\npython-dotenv",
          ".env.example": "DEBUG=true"
        }
      }
  }
  }
  