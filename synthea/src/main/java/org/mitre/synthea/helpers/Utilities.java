package org.mitre.synthea.helpers;

import com.google.common.base.Charsets;
import com.google.common.io.Resources;
import com.google.gson.FieldNamingPolicy;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonPrimitive;

import java.io.IOException;
import java.net.URL;
import java.util.Calendar;
import java.util.Random;
import java.util.TimeZone;
import java.util.concurrent.TimeUnit;

import org.mitre.synthea.engine.Logic;
import org.mitre.synthea.engine.State;
import org.mitre.synthea.world.concepts.HealthRecord.Code;

public class Utilities {
  /**
   * Convert a quantity of time in a specified units into milliseconds.
   *
   * @param units
   *          : "hours", "minutes", "seconds", "days", "weeks", "years", or "months"
   * @param value
   *          : quantity of units
   * @return milliseconds
   */
  public static long convertTime(String units, long value) {
    switch (units) {
      case "hours":
        return TimeUnit.HOURS.toMillis(value);
      case "minutes":
        return TimeUnit.MINUTES.toMillis(value);
      case "seconds":
        return TimeUnit.SECONDS.toMillis(value);
      case "days":
        return TimeUnit.DAYS.toMillis(value);
      case "years":
        return TimeUnit.DAYS.toMillis(365 * value);
      case "months":
        return TimeUnit.DAYS.toMillis(30 * value);
      case "weeks":
        return TimeUnit.DAYS.toMillis(7 * value);
      default:
        throw new RuntimeException("Unexpected time unit: " + units);
    }
  }

  public static long convertCalendarYearsToTime(int years) {
    return convertTime("years", (long) (years - 1970));
  }

  public static int getYear(long time) {
    Calendar calendar = Calendar.getInstance(TimeZone.getTimeZone("UTC"));
    calendar.setTimeInMillis(time);
    return calendar.get(Calendar.YEAR);
  }

  public static int getMonth(long time) {
    Calendar calendar = Calendar.getInstance(TimeZone.getTimeZone("UTC"));
    calendar.setTimeInMillis(time);
    return calendar.get(Calendar.MONTH) + 1;
  }

  /**
   * Converts a JsonPrimitive into a primitive Boolean, Double, or String.
   *
   * @param p
   *          : JsonPrimitive
   * @return Boolean, Double, or String
   */
  public static Object primitive(JsonPrimitive p) {
    Object retVal = null;
    if (p.isBoolean()) {
      retVal = p.getAsBoolean();
    } else if (p.isNumber()) {
      double doubleVal = p.getAsDouble();

      if (doubleVal == Math.rint(doubleVal)) {
        retVal = (int) doubleVal;
      } else {
        retVal = doubleVal;
      }
    } else if (p.isString()) {
      retVal = p.getAsString();
    }
    return retVal;
  }

  public static double convertRiskToTimestep(double risk, double originalPeriodInMS) {
    double currTimeStepInMS = Double.parseDouble(Config.get("generate.timestep"));

    return 1 - Math.pow(1 - risk, currTimeStepInMS / originalPeriodInMS);
  }

  public static boolean compare(Object lhs, Object rhs, String operator) {
    if (operator.equals("is nil")) {
      return lhs == null;
    } else if (operator.equals("is not nil")) {
      return lhs != null;
    } else if (lhs == null) {
      return false;
    }
    if (lhs instanceof Number && rhs instanceof Number) {
      return compare(((Number) lhs).doubleValue(), ((Number) rhs).doubleValue(), operator);
    } else if (lhs instanceof Boolean && rhs instanceof Boolean) {
      return compare((Boolean) lhs, (Boolean) rhs, operator);
    } else if (lhs instanceof String && rhs instanceof String) {
      return compare((String) lhs, (String) rhs, operator);
    } else if (lhs instanceof Code && rhs instanceof Code) {
      return compare((Code) lhs, (Code) rhs, operator);
    } else {
      throw new RuntimeException(String.format("Cannot compare %s to %s.\n",
          lhs.getClass().getName(), rhs.getClass().getName()));
    }
  }

  public static boolean compare(Double lhs, Double rhs, String operator) {
    switch (operator) {
      case "<":
        return lhs < rhs;
      case "<=":
        return lhs <= rhs;
      case "==":
        return lhs.doubleValue() == rhs.doubleValue();
      case ">=":
        return lhs >= rhs;
      case ">":
        return lhs > rhs;
      case "!=":
        return lhs.doubleValue() != rhs.doubleValue();
      case "is nil":
        return lhs == null;
      case "is not nil":
        return lhs != null;
      default:
        System.err.format("Unsupported operator: %s\n", operator);
        return false;
    }
  }

  public static boolean compare(Boolean lhs, Boolean rhs, String operator) {
    switch (operator) {
      case "<":
        return lhs != rhs;
      case "<=":
        return lhs != rhs;
      case "==":
        return lhs == rhs;
      case ">=":
        return lhs != rhs;
      case ">":
        return lhs != rhs;
      case "!=":
        return lhs != rhs;
      case "is nil":
        return lhs == null;
      case "is not nil":
        return lhs != null;
      default:
        System.err.format("Unsupported operator: %s\n", operator);
        return false;
    }
  }

  public static boolean compare(String lhs, String rhs, String operator) {
    switch (operator) {
      case "<":
        return lhs.compareTo(rhs) < 0;
      case "<=":
        return lhs.compareTo(rhs) <= 0;
      case "==":
        return lhs == rhs;
      case ">=":
        return lhs.compareTo(rhs) >= 0;
      case ">":
        return lhs.compareTo(rhs) > 0;
      case "!=":
        return lhs != rhs;
      case "is nil":
        return lhs == null;
      case "is not nil":
        return lhs != null;
      default:
        System.err.format("Unsupported operator: %s\n", operator);
        return false;
    }
  }

  public static boolean compare(Integer lhs, Integer rhs, String operator) {
    switch (operator) {
      case "<":
        return lhs < rhs;
      case "<=":
        return lhs <= rhs;
      case "==":
        return lhs.intValue() == rhs.intValue();
      case ">=":
        return lhs >= rhs;
      case ">":
        return lhs > rhs;
      case "!=":
        return lhs.intValue() != rhs.intValue();
      case "is nil":
        return lhs == null;
      case "is not nil":
        return lhs != null;
      default:
        System.err.format("Unsupported operator: %s\n", operator);
        return false;
    }
  }

  public static boolean compare(Code lhs, Code rhs, String operator) {
    switch (operator) {
      case "==":
        return lhs.equals(rhs);
      case "!=":
        return !lhs.equals(rhs);
      case "is nil":
        return lhs == null;
      case "is not nil":
        return lhs != null;
      default:
        System.err.format("Unsupported operator: %s\n", operator);
        return false;
    }
  }

  /**
   * The version identifier from the current version of Synthea.
   * Pulled from an autogenerated version file.
   */
  public static final String SYNTHEA_VERSION = getSyntheaVersion();

  private static String getSyntheaVersion() {
    String version = "synthea-java"; // reasonable default if we can't find a better one

    try {
      // see build.gradle for version.txt format
      String text = readResource("version.txt");
      if (text != null && text.length() > 0) {
        version = text;
      }
    } catch (Exception e) {
      // don't crash if the file isn't there, or for any other reason
      e.printStackTrace();
    }
    return version;
  }

  /**
   * Read the entire contents of a file in resources into a String.
   * @param filename Path to the file, relative to src/main/resources.
   * @return The entire text contents of the file.
   * @throws IOException if any error occurs reading the file
   */
  public static final String readResource(String filename) throws IOException {
    URL url = Resources.getResource(filename);
    return Resources.toString(url, Charsets.UTF_8);
  }

  /**
   * Get a Gson object, preconfigured to load the GMF modules into classes.
   *
   * @return Gson object to unmarshal GMF JSON into objects
   */
  public static Gson getGson() {
    return new GsonBuilder()
      .setFieldNamingPolicy(FieldNamingPolicy.LOWER_CASE_WITH_UNDERSCORES)
      .registerTypeAdapterFactory(InnerClassTypeAdapterFactory.of(Logic.class,"condition_type"))
      .registerTypeAdapterFactory(InnerClassTypeAdapterFactory.of(State.class, "type"))
      .create();
  }

  /**
   * Generate a random DICOM UID to uniquely identify an ImagingStudy, Series, or Instance.
   * Optionally add series and/or instance numbers to the UID to enhance its uniqueness.
   * Pass 0 for the series/instance number to omit it from the UID.
   *
   * @return a String DICOM UID
   */
  public static String randomDicomUid(int seriesNo, int instanceNo) {

    // Add a random salt to increase uniqueness
    String salt = randomDicomUidSalt();

    String now = String.valueOf(System.currentTimeMillis());
    String uid = "1.2.840.99999999";  // 99999999 is an arbitrary organizational identifier

    if (seriesNo > 0) {
      uid += "." + String.valueOf(seriesNo);
    }

    if (instanceNo > 0) {
      uid += "." + String.valueOf(instanceNo);
    }

    return uid + "." + salt + "." + now;
  }

  /**
   * Generates a random string of 8 numbers to use as a salt for DICOM UIDs.
   * @return The 8-digit numeric salt, as a String
   */
  private static String randomDicomUidSalt() {

    final int MIN = 10000000;
    final int MAX = 99999999;

    Random rand = new Random();
    int saltInt = rand.nextInt(MAX - MIN + 1) + MIN;
    return String.valueOf(saltInt);
  }
}
