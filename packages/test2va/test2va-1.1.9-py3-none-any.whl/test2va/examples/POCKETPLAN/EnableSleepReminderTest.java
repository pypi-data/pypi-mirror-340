package com.pocket_plan.j7_003.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.closeSoftKeyboard;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.action.ViewActions.scrollTo;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.hasDescendant;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withParentIndex;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.is;

import androidx.test.espresso.matcher.ViewMatchers;
import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import com.pocket_plan.j7_003.MainActivity;
import com.pocket_plan.j7_003.R;

import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class EnableSleepReminderTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void enableSleepReminderTest() throws InterruptedException {
        onView(allOf(withContentDescription("open"), withParent(ViewMatchers.withId(R.id.tbMain))))
                .perform(click());

        onView(allOf(withId(R.id.menuSleepReminder),  hasDescendant(withText("Sleep Reminder"))))
                .perform(click());

        onView(withId(R.id.switchEnableReminder)).perform(click());
        onView(allOf(withId(R.id.bottom3), withContentDescription("Home"))).perform(click());

        onView(withId(R.id.icSleepHome)).check(matches(isDisplayed()));
    }
}
