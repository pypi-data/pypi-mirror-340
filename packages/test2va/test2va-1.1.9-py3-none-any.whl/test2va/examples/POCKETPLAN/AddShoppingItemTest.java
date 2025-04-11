package com.pocket_plan.j7_003.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.Espresso.pressBack;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.closeSoftKeyboard;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.action.ViewActions.typeText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.anything;
import static org.hamcrest.Matchers.containsStringIgnoringCase;
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
public class AddShoppingItemTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void addShoppingItemTest() throws InterruptedException {
        onView(allOf(withId(R.id.bottom4),
                withContentDescription("Shopping")))
                .perform(click());

        onView(withId(R.id.btnAdd)).perform(click());
        onView(allOf(withId(R.id.actvItem))).perform(typeText("Apple"));
        onView(withId(R.id.etItemAmount)).perform(replaceText("5"));
        pressBack();
        onView(allOf(withId(R.id.btnAddItemToList), withText("ADD"))).perform(click());
        Thread.sleep(2000);
        pressBack();
        pressBack();

        Thread.sleep(2000);
        onView(allOf(withId(R.id.tvItemTitle), withText(containsStringIgnoringCase("5x Apple"))))
                .check(matches(isDisplayed()));
    }
}
