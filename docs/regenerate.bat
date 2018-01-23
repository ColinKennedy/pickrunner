set ROOT=%~dp0
echo %ROOT:~0,-1%
sphinx-apidoc -f -o %ROOT%source %ROOT%..\scripts\pickrunner
