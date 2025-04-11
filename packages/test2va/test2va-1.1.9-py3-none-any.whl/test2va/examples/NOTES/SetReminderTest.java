package com.maltaisn.notes.test2va;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsString;

import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import com.maltaisn.notes.R;
import com.maltaisn.notes.ui.main.MainActivity;

import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class SetReminderTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void setReminderTest() {
        onView(allOf(withContentDescription("Open drawer"),
                isDisplayed())).perform(click());
        onView(allOf(withText("Reminders"),
                isDisplayed())).perform(click());
        onView(allOf(withId(R.id.fab), withContentDescription("Create note"),
                isDisplayed())).perform(click());
        onView(allOf(withId(R.id.time_input_layout),
                isDisplayed())).perform(click());

        //4 o'clock
        onView(allOf(withText("4"), withContentDescription("4 o'clock"),
                isDisplayed())).perform(click());
        //pm
        onView(allOf(withText("PM"), isDisplayed())).perform(click());
        onView(allOf(withText("OK"), isDisplayed())).perform(click());

        onView(withText(containsString("4"))).check(matches(isDisplayed()));
        onView(withText(containsString("PM"))).check(matches(isDisplayed()));
    }
}
