# Setup

## python virtual environment

Install pyenv to manage the Python version: https://github.com/pyenv/pyenv


```sh 
pyenv install 3.12.4
pyenv local 3.12.4

python -m venv .venv
source .venv/bin/activate

```


## Reflex
https://reflex.dev/docs/getting-started/installation/ 

```

<!-- pip install reflex -->
<!-- reflex init  -->
pip -r requirements.txt
```

choose the free template (0)


## run it in development mode

```
reflex db init 
reflex run
```

url: http://localhost:3000


# References 

https://github.com/masenf/reflex-local-auth
https://reflex.dev/templates/
