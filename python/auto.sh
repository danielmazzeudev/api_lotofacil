REPO_DIR="/home/lumni/Documents/GitHub/api_lotofacil"
PYTHON_PATH="/usr/bin/python3"
SCRIPT_PATH="$REPO_DIR/python/lotofacil.py"

cd "$REPO_DIR" || exit

echo "Iniciando script Python em $(date)..."

$PYTHON_PATH $SCRIPT_PATH && {
    echo "Python finalizado com sucesso. Iniciando Git Push..."

    git add .
    
    if git diff-index --quiet HEAD --; then
        echo "Nenhuma mudança detectada nos arquivos. Pulando push."
    else
        git commit -m "Auto-commit: atualização via script em $(date)"
        git push origin main
        echo "Git push concluído com sucesso!"
    fi
} || {
    echo "Erro: O script Python falhou ou foi interrompido. Git Push cancelado."
    exit 1
}