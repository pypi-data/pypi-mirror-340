package com.pocket_plan.j7_003.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.closeSoftKeyboard;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.action.ViewActions.swipeLeft;
import static androidx.test.espresso.assertion.ViewAssertions.doesNotExist;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.hasDescendant;
import static androidx.test.espresso.matcher.ViewMatchers.isChecked;
import static androidx.test.espresso.matcher.ViewMatchers.isNotChecked;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;

import androidx.test.espresso.matcher.ViewMatchers;
import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import com.pocket_plan.j7_003.MainActivity;
import com.pocket_plan.j7_003.R;

import org.hamcrest.Matchers;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class CheckToDoTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Before
    public void Prepare() {
        onView(allOf(withId(R.id.bottom2), withContentDescription("To-Do")))
                .perform(click());
        onView(withId(R.id.btnAdd)).perform(click());
        onView(withId(R.id.etTitleAddTask))
                .perform(replaceText("Call doctor"));
        closeSoftKeyboard();
        onView(allOf(withId(R.id.btnConfirm1), withText("1"))).perform(click());

        onView(withId(R.id.btnAdd)).perform(click());
        onView(withId(R.id.etTitleAddTask))
                .perform(replaceText("Go shopping"));
        closeSoftKeyboard();
        onView(allOf(withId(R.id.btnConfirm2), withText("2"))).perform(click());
    }

    @Test
    public void checkToDoTest() {

        onView(allOf(withId(R.id.bottom2), withContentDescription("To-Do")))
                .perform(click());

        onView(allOf(withId(R.id.cbTask),
                withParent(allOf(withId(R.id.tapField),
                        withParent(hasDescendant(withText("Call doctor")))))))
                .perform(click());

        onView(allOf(withId(R.id.cbTask),
                withParent(allOf(withId(R.id.tapField),
                        withParent(hasDescendant(withText("Call doctor")))))))
                .check(matches(isChecked()));

    }

}
