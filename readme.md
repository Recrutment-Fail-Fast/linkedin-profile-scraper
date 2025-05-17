Stop-Process -Name chrome -Force
tasklist /FI "IMAGENAME eq chrome.exe"



irm https://astral.sh/uv/install.ps1 | iex


uv venv   

.venv\Scripts\activate  

uv install browser-use       

playwright install

chrome://version/


& "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --user-data-dir="C:\Users\juans\AppData\Local\Google\Chrome\User Data"

 & "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --user-data-dir="C:\Users\juans\AppData\Local\Google\Chrome\User Data\Profile 4"