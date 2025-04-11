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

import com.maltaisn.notes.ui.main.MainActivity;

import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class SetLeftSwipeToDeleteTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void setLeftSwipeToDeleteTest() {
        onView(allOf(withContentDescription("Open drawer"),
                isDisplayed())).perform(click());
        onView(allOf(withText("Settings"),
                isDisplayed())).perform(click());
        onView(allOf(withText(containsString("Swipe left")),
                isDisplayed())).perform(click());
        onView(allOf(withId(android.R.id.text1), withText("Delete"), isDisplayed())).perform(click());

        onView(allOf(withId(android.R.id.summary),
                withText("Delete"))).check(matches(isDisplayed()));
    }
}
