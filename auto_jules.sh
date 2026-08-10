#!/bin/bash

# Array of tasks covering Phase 2 (Civilization), Phase 3 (Economy), and Phase 4 (UI/Network)
TASKS=(
  # --- Phase 2: Civilization & Pathfinding ---
  "Implement a terrain-weighted Dijkstra shortest path solver on the Voronoi cell graph for culture and state expansion to shape realistic political borders. Reference culture-generator.ts and state-generator.ts."
  "Add placement rating equations to burg-generator.ts to calculate harbors, crossroads, defensive layouts, and capital status."
  "Implement A* search pathfinding in route-generator.ts to map land trails, main roads, and sea lanes connecting the generated burgs."
  
  # --- Phase 3: The Economy ---
  "Migrate detailed goods catalogs, production resource inputs, and specific raw vs manufactured tags into goods-generator.ts."
  "Implement equations in production-generator.ts to calculate production volumes, consumption, sales taxes, and treasuries."
  
  # --- Phase 4: Interface & Networking ---
  "Refactor the remaining monolithic HTML elements, such as the Route Painter, into modular UI widgets within the frontend/ui directory."
  "Complete the WebSocket server integration in the backend/main.py to fully support real-time multiplayer map collaboration."
)

echo "Starting automated Jules task sequence..."
echo "--------------------------------------------------"

for TASK in "${TASKS[@]}"; do
  echo "Initiating task: $TASK"
  
  # Start the session and extract the Session ID using grep
  SESSION_ID=$(jules remote new --repo . --session "$TASK" | grep -oE '[0-9a-zA-Z_-]+$')
  
  # Safety check in case the session fails to start
  if [ -z "$SESSION_ID" ]; then
    echo "Error: Failed to start session or retrieve Session ID. Exiting sequence."
    exit 1
  fi

  echo "Jules is working in the cloud on session: $SESSION_ID"

  # Polling loop to wait for the task to finish
  while true; do
    # Fetch the status of the specific session using awk to grab the last column
    STATUS=$(jules remote list --session | grep "$SESSION_ID" | awk '{print $NF}')
    
    # Check if the status has reached a terminal state
    if [[ "$STATUS" == "Completed" || "$STATUS" == "Failed" || "$STATUS" == "Merged" ]]; then
      echo "Session $SESSION_ID finished with status: $STATUS"
      
      # If the task failed, you may want to halt the script to investigate
      if [[ "$STATUS" == "Failed" ]]; then
        echo "Task failed. Halting automation so you can review."
        exit 1
      fi
      
      break
    fi
    
    echo "Waiting for Jules... Checking again in 30 seconds."
    sleep 30
  done
  
  # Bring the resulting changes back to your local environment
  echo "Pulling local patch for $SESSION_ID..."
  jules remote pull --session "$SESSION_ID"

  echo "Task complete. Moving to the next task..."
  echo "--------------------------------------------------"
done

echo "All automated tasks in the sequence have been processed."