package com.pocket_plan.j7_003.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.Espresso.pressBack;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.closeSoftKeyboard;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.action.ViewActions.typeText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.hasDescendant;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.containsStringIgnoringCase;
import static org.hamcrest.Matchers.is;

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
public class SearchShoppingItemTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Before
    public void prepare() throws InterruptedException {
        onView(allOf(withId(R.id.bottom4),
                withContentDescription("Shopping")))
                .perform(click());

        onView(withId(R.id.btnAdd)).perform(click());

        // add apple
        onView(allOf(withId(R.id.actvItem))).perform(typeText("Apple"));
        pressBack();
        Thread.sleep(1000);
        onView(withId(R.id.etItemAmount)).perform(replaceText("5"));
        pressBack();
        Thread.sleep(1000);
        onView(allOf(withId(R.id.btnAddItemToList), withText("ADD"))).perform(click());


        // add water
        onView(allOf(withId(R.id.actvItem))).perform(typeText("Water"));
        pressBack();
        Thread.sleep(2000);
        onView(allOf(withId(R.id.btnAddItemToList), withText("ADD"))).perform(click());
        Thread.sleep(1000);

        // add apple juice
        onView(allOf(withId(R.id.actvItem))).perform(typeText("Apple juice"));
        pressBack();
        Thread.sleep(2000);
        onView(allOf(withId(R.id.btnAddItemToList), withText("ADD"))).perform(click());
        Thread.sleep(1000);

        // add milk
        onView(allOf(withId(R.id.actvItem))).perform(typeText("Milk"));
        pressBack();
        Thread.sleep(2000);
        onView(withId(R.id.etItemAmount)).perform(replaceText("2"));
        pressBack();
        onView(allOf(withId(R.id.btnAddItemToList), withText("ADD"))).perform(click());
        Thread.sleep(1000);

        pressBack();

    }

    @Test
    public void searchShoppingItemTest() throws InterruptedException {

        onView(allOf(withId(R.id.bottom4),
                withContentDescription("Shopping")))
                .perform(click());

        onView(allOf(withId(R.id.item_shopping_search),
                hasDescendant(withContentDescription("Search")))).perform(click());
        Thread.sleep(8000);
        onView(withClassName(containsStringIgnoringCase("EditText")))
                .perform(typeText("Apple"));

        onView(withId(R.id.recycler_view_shopping)).check(matches(isDisplayed()));
    }
}
