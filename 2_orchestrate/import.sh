#!/bin/bash

echo "==========================================="
echo "   Importing all Watsonx Orchestrate tools  "
echo "==========================================="

TOOLS_DIR="tools"

# Controlla che la cartella tools esista
if [ ! -d "$TOOLS_DIR" ]; then
    echo "❌ Folder 'tools/' not found. Abort."
    exit 1
fi

# Loop di importazione per ogni file .py
for TOOL_FILE in $TOOLS_DIR/*.py; do
    echo "-------------------------------------------"
    echo "📦 Importing tool from file: $TOOL_FILE"
    echo "-------------------------------------------"

    orchestrate tools import \
        -k python \
        -f "$TOOL_FILE"

    STATUS=$?
    if [ $STATUS -ne 0 ]; then
        echo "❌ Error importing $TOOL_FILE"
        exit 1
    else
        echo "✅ Successfully imported: $TOOL_FILE"
    fi
done

echo "==========================================="
echo "🎉 All tools imported successfully!"
echo "==========================================="

#!/bin/bash

echo "==========================================="
echo "   Importing all Watsonx Orchestrate agents "
echo "==========================================="

AGENTS_DIR="agents"

# Check folder exists
if [ ! -d "$AGENTS_DIR" ]; then
    echo "❌ Folder 'agents/' not found. Abort."
    exit 1
fi

# Loop over all YAML files in agents/
for AGENT_FILE in $AGENTS_DIR/*.yaml; do
    echo "-------------------------------------------"
    echo "🤖 Importing agent from file: $AGENT_FILE"
    echo "-------------------------------------------"

    orchestrate agents import \
        -f "$AGENT_FILE"

    STATUS=$?
    if [ $STATUS -ne 0 ]; then
        echo "❌ Error importing $AGENT_FILE"
        exit 1
    else
        echo "✅ Successfully imported: $AGENT_FILE"
    fi
done

echo "==========================================="
echo "🎉 All agents imported successfully!"
echo "==========================================="
