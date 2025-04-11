package com.pocket_plan.j7_003.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.scrollTo;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isNotChecked;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsString;
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
public class DisableCollapseListTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void disableCollapseListTest() {
        onView(withContentDescription("open")).perform(click());
        onView(withId(R.id.menuItemSettings)).perform(click());
        onView(withId(R.id.clSettingShopping)).perform(scrollTo());
        onView(withId(R.id.clSettingShopping)).perform(click());
        onView(withId(R.id.swCollapseCheckedSublists)).perform(click());

        onView(allOf(withId(R.id.swCollapseCheckedSublists),
                withClassName(containsString("Switch"))))
                .check(matches(isNotChecked()));

    }

}
