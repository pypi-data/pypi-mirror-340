package com.maltaisn.notes.test2va;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.swipeRight;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;

import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import com.maltaisn.notes.R;
import com.maltaisn.notes.ui.main.MainActivity;

import org.junit.After;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class CheckNumberOfLabelsInPreviewTest {

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
    public void checkNumberOfLabelsInPreviewTest() {

        onView(withContentDescription("Open drawer")).perform(click());
        onView(withId(R.id.drawer_item_settings)).perform(click());

        onView(withId(androidx.preference.R.id.seekbar_value)).check(matches(withText("2")));



    }
}
