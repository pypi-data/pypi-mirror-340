package com.pocket_plan.j7_003.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.closeSoftKeyboard;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.action.ViewActions.scrollTo;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.is;

import androidx.test.espresso.matcher.ViewMatchers;
import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import com.pocket_plan.j7_003.MainActivity;
import com.pocket_plan.j7_003.R;

import org.hamcrest.Matchers;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class AddBirthdayTodayTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void addBirthdayTodayTest() {

        onView(allOf(withId(R.id.bottom5),
                withContentDescription("Birthdays"))).perform(click());

        onView(withId(R.id.btnAdd)).perform(click());

        onView(withText(containsStringIgnoringCase("Name (Date)"))).perform(replaceText("Jenny"));
        closeSoftKeyboard();

        onView(allOf(withId(R.id.tvBirthdayDate), withText("Choose date")))
                .perform(click());

        onView(allOf(withId(android.R.id.button1), withText("OK"))).perform(scrollTo());
        onView(allOf(withId(android.R.id.button1), withText("OK"))).perform(click());

        onView(allOf(withId(R.id.btnConfirmBirthday), withText("ADD")))
                .perform(click());

        onView(allOf(withId(R.id.tvRowBirthdayName), withText("Jenny")))
                .check(matches(withText("Jenny")));

        onView(allOf(withId(R.id.tvRowBirthdayDays), withText("today")))
                .check(matches(withText("today")));
    }
}
