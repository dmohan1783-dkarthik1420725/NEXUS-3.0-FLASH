@echo off
echo 🔱 VEDA 3.1 ULTRA: INITIATING DATA SYNC...

:: 1. Run the Deep Scout to generate the data
bun run "C:\VEDA\veda_cmd.ts" %* > C:\VEDA\latest_intel.txt

:: 2. Move the data to your GitHub folder (Change path to your actual GitHub folder)
copy C:\VEDA\latest_intel.txt C:\Users\MOHAN\Documents\GitHub\YourRepoName\data.txt

:: 3. Git Push Sequence
cd C:\Users\MOHAN\Documents\GitHub\YourRepoName
git add .
git commit -m "🔱 Neural Update: %DATE% %TIME%"
git push origin main

echo 🔱 VEDA 3.1 ULTRA: DATA PUSHED TO GITHUB. STREAMLIT UPDATING...