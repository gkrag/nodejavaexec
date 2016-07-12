@echo off

rem This is the path to Java. Edit this variable to suite your needs.

set JAVA=java
set CP="DigiAccessExtras.jar"

echo.
%JAVA% -cp %CP% "com.tcs.digi.extras."%*
echo.