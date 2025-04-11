package org.totschnig.myexpenses.test2va;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.isNotChecked;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsString;

import androidx.test.ext.junit.rules.ActivityScenarioRule;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.totschnig.myexpenses.activity.SplashActivity;

public class BackupTest {


    @Rule
    public ActivityScenarioRule<SplashActivity> rule = new ActivityScenarioRule<>(SplashActivity.class);

    @Before
    public void setup() {
        //OnboardingActivity
        onView(allOf(withText("Next"),
                isDisplayed())).perform(click());
        onView(allOf(withText("Next"),
                isDisplayed())).perform(click());
        onView(allOf(withText("Get started"),
                isDisplayed())).perform(click());
    }

    @Test
    public void backupTest() {
        onView(allOf(withContentDescription("More options"),
                isDisplayed())).perform(click());
        onView(allOf(withText("Settings"),
                isDisplayed())).perform(click());
        onView(allOf(withText("Backup / Restore"),
                isDisplayed())).perform(click());
        onView(allOf(withText("Backup"),
                isDisplayed())).perform(click());
        onView(allOf(withText("OK"),
                isNotChecked())).perform(click());

        onView(withText(containsString("successfully written"))).check(matches(isDisplayed()));

    }

}
