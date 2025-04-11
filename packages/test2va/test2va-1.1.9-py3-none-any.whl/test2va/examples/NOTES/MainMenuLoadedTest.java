package com.maltaisn.notes.test2va;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isClickable;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.isEnabled;
import static androidx.test.espresso.matcher.ViewMatchers.isNotClickable;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;

import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.not;

import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import com.maltaisn.notes.R;
import com.maltaisn.notes.ui.main.MainActivity;

import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.After;
import org.junit.Before;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class MainMenuLoadedTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);
    @Before
    public void waitForApp() throws InterruptedException {
        Thread.sleep(1500);

    }

    @After
    public void waitForResult() throws InterruptedException {
        Thread.sleep(1500);
    }

    @Test
    public void mainMenuLoadedTest() {
        onView(allOf(withContentDescription("Open drawer"),
                    isDisplayed())).perform(click());

        onView(withText("Settings")).check(matches(isDisplayed()));
        onView(withText("Reminders")).check(matches(isDisplayed()));
        onView(withText("Reminders")).check(matches(isNotClickable()));
        onView(withText("Reminders")).check(matches(not(isClickable())));
        onView(withId(R.id.drawer_item_create_label)).check(matches(isClickable()));
        onView(withId(R.id.drawer_item_create_label)).check(matches(isEnabled()));

    }

}
