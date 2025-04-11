package com.futsch1.medtimer.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.swipeLeft;
import static androidx.test.espresso.action.ViewActions.typeText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withParentIndex;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsStringIgnoringCase;

import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;

import androidx.test.espresso.matcher.ViewMatchers;
import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;
import androidx.test.rule.GrantPermissionRule;

import com.futsch1.medtimer.MainActivity;
import com.futsch1.medtimer.R;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.Matchers;
import org.hamcrest.TypeSafeMatcher;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class DeactivateRemindersTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Rule
    public GrantPermissionRule mGrantPermissionRule =
            GrantPermissionRule.grant(
                    "android.permission.POST_NOTIFICATIONS");

    @Before
    public void prepare() throws InterruptedException {
        Thread.sleep(3000);
        onView(withText(containsStringIgnoringCase("skip"))).perform(click());

        onView(allOf(withId(R.id.medicinesFragment),
                withContentDescription("Medicine"))).perform(click());

        onView(allOf(withId(R.id.addMedicine), withText("Add medicine"))).perform(click());
        onView(withClassName(containsStringIgnoringCase("EditText")))
                .perform(typeText("B12"));

        onView(allOf(withId(android.R.id.button1), withText("OK"))).perform(click());

        onView(allOf(withId(R.id.addMedicine), withText("Add medicine"))).perform(click());
        onView(withClassName(containsStringIgnoringCase("EditText")))
                .perform(typeText("Omega3"));

        onView(allOf(withId(android.R.id.button1), withText("OK"))).perform(click());

        // add reminder for B12
        onView(allOf(withId(R.id.medicinesFragment), withContentDescription("Medicine"))).perform(click());

        onView(allOf(withId(R.id.medicineName), withText("B12"))).perform(click());
        onView(allOf(withId(R.id.addReminder), withText("Add reminder"))).perform(click());

        onView(withClassName(containsStringIgnoringCase("EditText")))
                .perform(typeText("1000 mcg"));
        onView(allOf(withId(android.R.id.button1), withText("OK"))).perform(click());
        Thread.sleep(1000);

        onView(allOf(withText("10"), withContentDescription("10 o'clock"),
                withParent(withId(com.google.android.material.R.id.material_clock_face)))).perform(click());
        onView(allOf(withText("30"), withContentDescription("30 minutes"),
                withParent(withId(com.google.android.material.R.id.material_clock_face)))).perform(click());
        onView(withId(com.google.android.material.R.id.material_clock_period_am_button)).perform(click());
        onView(allOf(withId(com.google.android.material.R.id.material_timepicker_ok_button),
                withText("OK"))).perform(click());

        onView(allOf(withId(R.id.medicinesFragment), withContentDescription("Medicine"))).perform(click());

        // add reminder for Omega3
        onView(allOf(withId(R.id.medicineName), withText("Omega3"))).perform(click());
        onView(allOf(withId(R.id.addReminder), withText("Add reminder"))).perform(click());

        onView(withClassName(containsStringIgnoringCase("EditText")))
                .perform(typeText("1200 mg"));
        onView(allOf(withId(android.R.id.button1), withText("OK"))).perform(click());
        Thread.sleep(1000);

        onView(allOf(withText("10"), withContentDescription("10 o'clock"),
                withParent(withId(com.google.android.material.R.id.material_clock_face)))).perform(click());
        onView(allOf(withText("30"), withContentDescription("30 minutes"),
                withParent(withId(com.google.android.material.R.id.material_clock_face)))).perform(click());
        onView(withId(com.google.android.material.R.id.material_clock_period_pm_button)).perform(click());
        onView(allOf(withId(com.google.android.material.R.id.material_timepicker_ok_button),
                withText("OK"))).perform(click());
    }

    @Test
    public void deactivateRemindersTest() throws InterruptedException {

        onView(allOf(withId(R.id.medicinesFragment), withContentDescription("Medicine"))).perform(click());
        onView(allOf(withId(R.id.medicineName), withText("B12"))).perform(click());
        onView( withContentDescription("More options")).perform(click());
        Thread.sleep(2000);

        onView(allOf(withText("Deactivate all reminders")))
                .perform(click());
        onView(allOf(withId(R.id.advancedSettingsSummary),
                withText(containsStringIgnoringCase("Inactive")))).check(matches(isDisplayed()));

    }

}
