Stop-Process -Name chrome -Force
tasklist /FI "IMAGENAME eq chrome.exe"



irm https://astral.sh/uv/install.ps1 | iex


uv venv   

.venv\Scripts\activate  

uv install browser-use       

playwright install

chrome://version/