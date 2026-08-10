$Tasks = @(
    # --- Phase 2: Civilization & Pathfinding ---
    "Implement a terrain-weighted Dijkstra shortest path solver on the Voronoi cell graph for culture and state expansion to shape realistic political borders. Reference culture-generator.ts and state-generator.ts.",
    "Add placement rating equations to burg-generator.ts to calculate harbors, crossroads, defensive layouts, and capital status.",
    "Implement A* search pathfinding in route-generator.ts to map land trails, main roads, and sea lanes connecting the generated burgs.",
    
    # --- Phase 3: The Economy ---
    "Migrate detailed goods catalogs, production resource inputs, and specific raw vs manufactured tags into goods-generator.ts.",
    "Implement equations in production-generator.ts to calculate production volumes, consumption, sales taxes, and treasuries.",
    
    # --- Phase 4: Interface & Networking ---
    "Refactor the remaining monolithic HTML elements, such as the Route Painter, into modular UI widgets within the frontend/ui directory.",
    "Complete the WebSocket server integration in the backend/main.py to fully support real-time multiplayer map collaboration."
)

Write-Host "Starting automated Jules task sequence..." -ForegroundColor Cyan
Write-Host "--------------------------------------------------" -ForegroundColor Cyan

foreach ($Task in $Tasks) {
    Write-Host "Initiating task: $Task" -ForegroundColor Yellow
    
    # Start the session and capture the output
    $startOutput = jules remote new --repo . --session "$Task"
    
    # Extract the Session ID (assuming it is the last string of alphanumeric/dash characters)
    $SessionId = [regex]::Match($startOutput, '[0-9a-zA-Z_-]+$').Value
    
    # Safety check in case the session fails to start
    if ([string]::IsNullOrWhiteSpace($SessionId)) {
        Write-Host "Error: Failed to start session or retrieve Session ID. Exiting sequence." -ForegroundColor Red
        exit
    }

    Write-Host "Jules is working in the cloud on session: $SessionId" -ForegroundColor Green

    # Polling loop to wait for the task to finish
    while ($true) {
        # Fetch the session list and filter for our specific ID
        $listOutput = jules remote list --session
        $statusLine = $listOutput | Select-String -Pattern $SessionId
        
        if ($statusLine) {
            # Split the line by whitespace and grab the last element (the status)
            $Status = ($statusLine -split '\s+')[-1]
            
            # Check if the status has reached a terminal state
            if ($Status -in @("Completed", "Failed", "Merged")) {
                Write-Host "Session $SessionId finished with status: $Status" -ForegroundColor Magenta
                
                # If the task failed, halt the script to investigate
                if ($Status -eq "Failed") {
                    Write-Host "Task failed. Halting automation so you can review." -ForegroundColor Red
                    exit
                }
                
                break
            }
        }
        
        Write-Host "Waiting for Jules... Checking again in 30 seconds." -ForegroundColor DarkGray
        Start-Sleep -Seconds 30
    }
    
    # Bring the resulting changes back to your local environment
    Write-Host "Pulling local patch for $SessionId..." -ForegroundColor Blue
    jules remote pull --session "$SessionId"

    Write-Host "Task complete. Moving to the next task..." -ForegroundColor Green
    Write-Host "--------------------------------------------------" -ForegroundColor Cyan
}

Write-Host "All automated tasks in the sequence have been processed." -ForegroundColor Green