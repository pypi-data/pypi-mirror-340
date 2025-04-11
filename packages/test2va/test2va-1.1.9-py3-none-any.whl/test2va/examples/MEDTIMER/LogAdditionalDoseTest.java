package com.futsch1.medtimer.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.action.ViewActions.typeText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.hasDescendant;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParentIndex;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsStringIgnoringCase;

import androidx.test.espresso.matcher.ViewMatchers;
import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;
import androidx.test.rule.GrantPermissionRule;

import com.futsch1.medtimer.MainActivity;
import com.futsch1.medtimer.R;

import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class LogAdditionalDoseTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Rule
    public GrantPermissionRule mGrantPermissionRule =
            GrantPermissionRule.grant(
                    "android.permission.POST_NOTIFICATIONS");

    @Before
    public void prepare() {
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
    }

    @Test
    public void logAdditionalDoseTest() {
        onView(allOf(withId(R.id.overviewFragment), withContentDescription("Overview")))
                .perform(click());
        onView(allOf(withId(R.id.logManualDose),
                withText("Log additional dose"))).perform(click());
        onView(allOf(withText("B12"), withId(android.R.id.text1)))
                .perform(click());
        onView(withClassName(containsStringIgnoringCase("EditText"))).
                perform(replaceText("500 mcg"));
        onView(allOf(withText("OK"), withId(android.R.id.button1))).perform(click());
        onView(withId(com.google.android.material.R.id.material_timepicker_ok_button)).perform(click());

        onView(allOf(withClassName(containsStringIgnoringCase("CardView")),
                withParentIndex(0), hasDescendant(withText("500 mcg of B12"))))
                .check(matches(isDisplayed()));
    }

}
