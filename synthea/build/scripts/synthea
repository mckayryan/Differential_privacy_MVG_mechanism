#!/usr/bin/env sh

##############################################################################
##
##  synthea start up script for UN*X
##
##############################################################################

# Attempt to set APP_HOME
# Resolve links: $0 may be a link
PRG="$0"
# Need this for relative symlinks.
while [ -h "$PRG" ] ; do
    ls=`ls -ld "$PRG"`
    link=`expr "$ls" : '.*-> \(.*\)$'`
    if expr "$link" : '/.*' > /dev/null; then
        PRG="$link"
    else
        PRG=`dirname "$PRG"`"/$link"
    fi
done
SAVED="`pwd`"
cd "`dirname \"$PRG\"`/.." >/dev/null
APP_HOME="`pwd -P`"
cd "$SAVED" >/dev/null

APP_NAME="synthea"
APP_BASE_NAME=`basename "$0"`

# Add default JVM options here. You can also use JAVA_OPTS and SYNTHEA_OPTS to pass JVM options to this script.
DEFAULT_JVM_OPTS=""

# Use the maximum available, or set MAX_FD != -1 to use that value.
MAX_FD="maximum"

warn () {
    echo "$*"
}

die () {
    echo
    echo "$*"
    echo
    exit 1
}

# OS specific support (must be 'true' or 'false').
cygwin=false
msys=false
darwin=false
nonstop=false
case "`uname`" in
  CYGWIN* )
    cygwin=true
    ;;
  Darwin* )
    darwin=true
    ;;
  MINGW* )
    msys=true
    ;;
  NONSTOP* )
    nonstop=true
    ;;
esac

CLASSPATH=$APP_HOME/lib/synthea.jar:$APP_HOME/lib/hapi-fhir-structures-dstu3-3.7.0-SNAPSHOT.jar:$APP_HOME/lib/hapi-fhir-structures-dstu2-3.7.0-SNAPSHOT.jar:$APP_HOME/lib/hapi-fhir-structures-r4-3.7.0-SNAPSHOT.jar:$APP_HOME/lib/hapi-fhir-utilities-3.7.0-SNAPSHOT.jar:$APP_HOME/lib/hapi-fhir-base-3.7.0-SNAPSHOT.jar:$APP_HOME/lib/gson-2.8.5.jar:$APP_HOME/lib/freemarker-2.3.26-incubating.jar:$APP_HOME/lib/sis-storage-0.8.jar:$APP_HOME/lib/sis-feature-0.8.jar:$APP_HOME/lib/sis-referencing-0.8.jar:$APP_HOME/lib/h2-1.4.196.jar:$APP_HOME/lib/guava-25.0-jre.jar:$APP_HOME/lib/graphviz-java-0.2.2.jar:$APP_HOME/lib/commons-csv-1.5.jar:$APP_HOME/lib/jackson-dataformat-csv-2.8.8.jar:$APP_HOME/lib/snakeyaml-1.19.jar:$APP_HOME/lib/commons-math3-3.6.1.jar:$APP_HOME/lib/commons-text-1.6.jar:$APP_HOME/lib/jaxb-runtime-2.3.1.jar:$APP_HOME/lib/jaxb-api-2.3.1.jar:$APP_HOME/lib/activation-1.1.1.jar:$APP_HOME/lib/slf4j-nop-1.6.1.jar:$APP_HOME/lib/jcl-over-slf4j-1.7.25.jar:$APP_HOME/lib/jul-to-slf4j-1.7.25.jar:$APP_HOME/lib/slf4j-api-1.7.25.jar:$APP_HOME/lib/commons-lang3-3.8.1.jar:$APP_HOME/lib/commons-codec-1.11.jar:$APP_HOME/lib/batik-codec-1.9.jar:$APP_HOME/lib/batik-rasterizer-1.9.jar:$APP_HOME/lib/batik-svgrasterizer-1.9.jar:$APP_HOME/lib/batik-transcoder-1.9.jar:$APP_HOME/lib/batik-bridge-1.9.jar:$APP_HOME/lib/batik-script-1.9.jar:$APP_HOME/lib/batik-anim-1.9.jar:$APP_HOME/lib/batik-svg-dom-1.9.jar:$APP_HOME/lib/batik-dom-1.9.jar:$APP_HOME/lib/batik-css-1.9.jar:$APP_HOME/lib/xmlgraphics-commons-2.2.jar:$APP_HOME/lib/commons-io-2.6.jar:$APP_HOME/lib/sis-metadata-0.8.jar:$APP_HOME/lib/sis-utility-0.8.jar:$APP_HOME/lib/geoapi-3.0.1.jar:$APP_HOME/lib/unit-api-1.0.jar:$APP_HOME/lib/j2v8_macosx_x86_64-4.6.0.jar:$APP_HOME/lib/j2v8_linux_x86_64-4.6.0.jar:$APP_HOME/lib/j2v8_win32_x86_64-4.6.0.jar:$APP_HOME/lib/j2v8_win32_x86-4.6.0.jar:$APP_HOME/lib/commons-exec-1.3.jar:$APP_HOME/lib/jackson-databind-2.8.8.jar:$APP_HOME/lib/jackson-core-2.8.8.jar:$APP_HOME/lib/jackson-annotations-2.8.0.jar:$APP_HOME/lib/jsr305-1.3.9.jar:$APP_HOME/lib/checker-compat-qual-2.0.0.jar:$APP_HOME/lib/error_prone_annotations-2.1.3.jar:$APP_HOME/lib/j2objc-annotations-1.1.jar:$APP_HOME/lib/animal-sniffer-annotations-1.14.jar:$APP_HOME/lib/txw2-2.3.1.jar:$APP_HOME/lib/istack-commons-runtime-3.0.7.jar:$APP_HOME/lib/stax-ex-1.8.jar:$APP_HOME/lib/FastInfoset-1.2.15.jar:$APP_HOME/lib/javax.activation-api-1.2.0.jar:$APP_HOME/lib/batik-parser-1.9.jar:$APP_HOME/lib/batik-gvt-1.9.jar:$APP_HOME/lib/batik-svggen-1.9.jar:$APP_HOME/lib/batik-awt-util-1.9.jar:$APP_HOME/lib/batik-xml-1.9.jar:$APP_HOME/lib/batik-util-1.9.jar:$APP_HOME/lib/xalan-2.7.2.jar:$APP_HOME/lib/serializer-2.7.2.jar:$APP_HOME/lib/xml-apis-1.3.04.jar:$APP_HOME/lib/batik-ext-1.9.jar:$APP_HOME/lib/xml-apis-ext-1.3.04.jar:$APP_HOME/lib/batik-constants-1.9.jar:$APP_HOME/lib/batik-i18n-1.9.jar:$APP_HOME/lib/commons-logging-1.0.4.jar

# Determine the Java command to use to start the JVM.
if [ -n "$JAVA_HOME" ] ; then
    if [ -x "$JAVA_HOME/jre/sh/java" ] ; then
        # IBM's JDK on AIX uses strange locations for the executables
        JAVACMD="$JAVA_HOME/jre/sh/java"
    else
        JAVACMD="$JAVA_HOME/bin/java"
    fi
    if [ ! -x "$JAVACMD" ] ; then
        die "ERROR: JAVA_HOME is set to an invalid directory: $JAVA_HOME

Please set the JAVA_HOME variable in your environment to match the
location of your Java installation."
    fi
else
    JAVACMD="java"
    which java >/dev/null 2>&1 || die "ERROR: JAVA_HOME is not set and no 'java' command could be found in your PATH.

Please set the JAVA_HOME variable in your environment to match the
location of your Java installation."
fi

# Increase the maximum file descriptors if we can.
if [ "$cygwin" = "false" -a "$darwin" = "false" -a "$nonstop" = "false" ] ; then
    MAX_FD_LIMIT=`ulimit -H -n`
    if [ $? -eq 0 ] ; then
        if [ "$MAX_FD" = "maximum" -o "$MAX_FD" = "max" ] ; then
            MAX_FD="$MAX_FD_LIMIT"
        fi
        ulimit -n $MAX_FD
        if [ $? -ne 0 ] ; then
            warn "Could not set maximum file descriptor limit: $MAX_FD"
        fi
    else
        warn "Could not query maximum file descriptor limit: $MAX_FD_LIMIT"
    fi
fi

# For Darwin, add options to specify how the application appears in the dock
if $darwin; then
    GRADLE_OPTS="$GRADLE_OPTS \"-Xdock:name=$APP_NAME\" \"-Xdock:icon=$APP_HOME/media/gradle.icns\""
fi

# For Cygwin, switch paths to Windows format before running java
if $cygwin ; then
    APP_HOME=`cygpath --path --mixed "$APP_HOME"`
    CLASSPATH=`cygpath --path --mixed "$CLASSPATH"`
    JAVACMD=`cygpath --unix "$JAVACMD"`

    # We build the pattern for arguments to be converted via cygpath
    ROOTDIRSRAW=`find -L / -maxdepth 1 -mindepth 1 -type d 2>/dev/null`
    SEP=""
    for dir in $ROOTDIRSRAW ; do
        ROOTDIRS="$ROOTDIRS$SEP$dir"
        SEP="|"
    done
    OURCYGPATTERN="(^($ROOTDIRS))"
    # Add a user-defined pattern to the cygpath arguments
    if [ "$GRADLE_CYGPATTERN" != "" ] ; then
        OURCYGPATTERN="$OURCYGPATTERN|($GRADLE_CYGPATTERN)"
    fi
    # Now convert the arguments - kludge to limit ourselves to /bin/sh
    i=0
    for arg in "$@" ; do
        CHECK=`echo "$arg"|egrep -c "$OURCYGPATTERN" -`
        CHECK2=`echo "$arg"|egrep -c "^-"`                                 ### Determine if an option

        if [ $CHECK -ne 0 ] && [ $CHECK2 -eq 0 ] ; then                    ### Added a condition
            eval `echo args$i`=`cygpath --path --ignore --mixed "$arg"`
        else
            eval `echo args$i`="\"$arg\""
        fi
        i=$((i+1))
    done
    case $i in
        (0) set -- ;;
        (1) set -- "$args0" ;;
        (2) set -- "$args0" "$args1" ;;
        (3) set -- "$args0" "$args1" "$args2" ;;
        (4) set -- "$args0" "$args1" "$args2" "$args3" ;;
        (5) set -- "$args0" "$args1" "$args2" "$args3" "$args4" ;;
        (6) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" ;;
        (7) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" "$args6" ;;
        (8) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" "$args6" "$args7" ;;
        (9) set -- "$args0" "$args1" "$args2" "$args3" "$args4" "$args5" "$args6" "$args7" "$args8" ;;
    esac
fi

# Escape application args
save () {
    for i do printf %s\\n "$i" | sed "s/'/'\\\\''/g;1s/^/'/;\$s/\$/' \\\\/" ; done
    echo " "
}
APP_ARGS=$(save "$@")

# Collect all arguments for the java command, following the shell quoting and substitution rules
eval set -- $DEFAULT_JVM_OPTS $JAVA_OPTS $SYNTHEA_OPTS -classpath "\"$CLASSPATH\"" App "$APP_ARGS"

# by default we should be in the correct project dir, but when run from Finder on Mac, the cwd is wrong
if [ "$(uname)" = "Darwin" ] && [ "$HOME" = "$PWD" ]; then
  cd "$(dirname "$0")"
fi

exec "$JAVACMD" "$@"
