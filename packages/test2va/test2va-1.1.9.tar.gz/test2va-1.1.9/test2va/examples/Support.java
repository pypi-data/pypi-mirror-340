package com.maltaisn.notes.test2va;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;

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
public class CreateLabelTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void createLabelTest() {

        String label = "Meeting";

        onView(allOf(withContentDescription("Open drawer"),
                isDisplayed())).perform(click());
        onView(allOf(withText("Create new label"),
                isDisplayed())).perform(click());
        onView(allOf(withId(R.id.label_input)))
                .perform(replaceText("Meeting"));
        onView(allOf(withId(android.R.id.button1), withText("OK"), isDisplayed())).perform(click());

        // TODO: nested matchers expect "onView", but that's not always the case
        // TODO: use https://www.programcreek.com/python/example/100022/selenium.webdriver.ActionChains
        // TODO: https://www.devstringx.com/automate-gestures-using-w3-actions-api-in-appium
        onView(allOf(withText(label),
                withParent(onView(withId(R.id.toolbar))))).check(matches(isDisplayed()));
    }
}
