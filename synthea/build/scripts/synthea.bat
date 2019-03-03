@if "%DEBUG%" == "" @echo off
@rem ##########################################################################
@rem
@rem  synthea startup script for Windows
@rem
@rem ##########################################################################

@rem Set local scope for the variables with windows NT shell
if "%OS%"=="Windows_NT" setlocal

set DIRNAME=%~dp0
if "%DIRNAME%" == "" set DIRNAME=.
set APP_BASE_NAME=%~n0
set APP_HOME=%DIRNAME%..

@rem Add default JVM options here. You can also use JAVA_OPTS and SYNTHEA_OPTS to pass JVM options to this script.
set DEFAULT_JVM_OPTS=

@rem Find java.exe
if defined JAVA_HOME goto findJavaFromJavaHome

set JAVA_EXE=java.exe
%JAVA_EXE% -version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto init

echo.
echo ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:findJavaFromJavaHome
set JAVA_HOME=%JAVA_HOME:"=%
set JAVA_EXE=%JAVA_HOME%/bin/java.exe

if exist "%JAVA_EXE%" goto init

echo.
echo ERROR: JAVA_HOME is set to an invalid directory: %JAVA_HOME%
echo.
echo Please set the JAVA_HOME variable in your environment to match the
echo location of your Java installation.

goto fail

:init
@rem Get command-line arguments, handling Windows variants

if not "%OS%" == "Windows_NT" goto win9xME_args

:win9xME_args
@rem Slurp the command line arguments.
set CMD_LINE_ARGS=
set _SKIP=2

:win9xME_args_slurp
if "x%~1" == "x" goto execute

set CMD_LINE_ARGS=%*

:execute
@rem Setup the command line

set CLASSPATH=%APP_HOME%\lib\synthea.jar;%APP_HOME%\lib\hapi-fhir-structures-dstu3-3.7.0-SNAPSHOT.jar;%APP_HOME%\lib\hapi-fhir-structures-dstu2-3.7.0-SNAPSHOT.jar;%APP_HOME%\lib\hapi-fhir-structures-r4-3.7.0-SNAPSHOT.jar;%APP_HOME%\lib\hapi-fhir-utilities-3.7.0-SNAPSHOT.jar;%APP_HOME%\lib\hapi-fhir-base-3.7.0-SNAPSHOT.jar;%APP_HOME%\lib\gson-2.8.5.jar;%APP_HOME%\lib\freemarker-2.3.26-incubating.jar;%APP_HOME%\lib\sis-storage-0.8.jar;%APP_HOME%\lib\sis-feature-0.8.jar;%APP_HOME%\lib\sis-referencing-0.8.jar;%APP_HOME%\lib\h2-1.4.196.jar;%APP_HOME%\lib\guava-25.0-jre.jar;%APP_HOME%\lib\graphviz-java-0.2.2.jar;%APP_HOME%\lib\commons-csv-1.5.jar;%APP_HOME%\lib\jackson-dataformat-csv-2.8.8.jar;%APP_HOME%\lib\snakeyaml-1.19.jar;%APP_HOME%\lib\commons-math3-3.6.1.jar;%APP_HOME%\lib\commons-text-1.6.jar;%APP_HOME%\lib\jaxb-runtime-2.3.1.jar;%APP_HOME%\lib\jaxb-api-2.3.1.jar;%APP_HOME%\lib\activation-1.1.1.jar;%APP_HOME%\lib\slf4j-nop-1.6.1.jar;%APP_HOME%\lib\jcl-over-slf4j-1.7.25.jar;%APP_HOME%\lib\jul-to-slf4j-1.7.25.jar;%APP_HOME%\lib\slf4j-api-1.7.25.jar;%APP_HOME%\lib\commons-lang3-3.8.1.jar;%APP_HOME%\lib\commons-codec-1.11.jar;%APP_HOME%\lib\batik-codec-1.9.jar;%APP_HOME%\lib\batik-rasterizer-1.9.jar;%APP_HOME%\lib\batik-svgrasterizer-1.9.jar;%APP_HOME%\lib\batik-transcoder-1.9.jar;%APP_HOME%\lib\batik-bridge-1.9.jar;%APP_HOME%\lib\batik-script-1.9.jar;%APP_HOME%\lib\batik-anim-1.9.jar;%APP_HOME%\lib\batik-svg-dom-1.9.jar;%APP_HOME%\lib\batik-dom-1.9.jar;%APP_HOME%\lib\batik-css-1.9.jar;%APP_HOME%\lib\xmlgraphics-commons-2.2.jar;%APP_HOME%\lib\commons-io-2.6.jar;%APP_HOME%\lib\sis-metadata-0.8.jar;%APP_HOME%\lib\sis-utility-0.8.jar;%APP_HOME%\lib\geoapi-3.0.1.jar;%APP_HOME%\lib\unit-api-1.0.jar;%APP_HOME%\lib\j2v8_macosx_x86_64-4.6.0.jar;%APP_HOME%\lib\j2v8_linux_x86_64-4.6.0.jar;%APP_HOME%\lib\j2v8_win32_x86_64-4.6.0.jar;%APP_HOME%\lib\j2v8_win32_x86-4.6.0.jar;%APP_HOME%\lib\commons-exec-1.3.jar;%APP_HOME%\lib\jackson-databind-2.8.8.jar;%APP_HOME%\lib\jackson-core-2.8.8.jar;%APP_HOME%\lib\jackson-annotations-2.8.0.jar;%APP_HOME%\lib\jsr305-1.3.9.jar;%APP_HOME%\lib\checker-compat-qual-2.0.0.jar;%APP_HOME%\lib\error_prone_annotations-2.1.3.jar;%APP_HOME%\lib\j2objc-annotations-1.1.jar;%APP_HOME%\lib\animal-sniffer-annotations-1.14.jar;%APP_HOME%\lib\txw2-2.3.1.jar;%APP_HOME%\lib\istack-commons-runtime-3.0.7.jar;%APP_HOME%\lib\stax-ex-1.8.jar;%APP_HOME%\lib\FastInfoset-1.2.15.jar;%APP_HOME%\lib\javax.activation-api-1.2.0.jar;%APP_HOME%\lib\batik-parser-1.9.jar;%APP_HOME%\lib\batik-gvt-1.9.jar;%APP_HOME%\lib\batik-svggen-1.9.jar;%APP_HOME%\lib\batik-awt-util-1.9.jar;%APP_HOME%\lib\batik-xml-1.9.jar;%APP_HOME%\lib\batik-util-1.9.jar;%APP_HOME%\lib\xalan-2.7.2.jar;%APP_HOME%\lib\serializer-2.7.2.jar;%APP_HOME%\lib\xml-apis-1.3.04.jar;%APP_HOME%\lib\batik-ext-1.9.jar;%APP_HOME%\lib\xml-apis-ext-1.3.04.jar;%APP_HOME%\lib\batik-constants-1.9.jar;%APP_HOME%\lib\batik-i18n-1.9.jar;%APP_HOME%\lib\commons-logging-1.0.4.jar

@rem Execute synthea
"%JAVA_EXE%" %DEFAULT_JVM_OPTS% %JAVA_OPTS% %SYNTHEA_OPTS%  -classpath "%CLASSPATH%" App %CMD_LINE_ARGS%

:end
@rem End local scope for the variables with windows NT shell
if "%ERRORLEVEL%"=="0" goto mainEnd

:fail
rem Set variable SYNTHEA_EXIT_CONSOLE if you need the _script_ return code instead of
rem the _cmd.exe /c_ return code!
if  not "" == "%SYNTHEA_EXIT_CONSOLE%" exit 1
exit /b 1

:mainEnd
if "%OS%"=="Windows_NT" endlocal

:omega
