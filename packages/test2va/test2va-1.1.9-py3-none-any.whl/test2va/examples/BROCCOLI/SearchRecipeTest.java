package com.flauschcode.broccoli.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isClickable;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsStringIgnoringCase;
import static org.hamcrest.Matchers.is;

import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import com.flauschcode.broccoli.MainActivity;
import com.flauschcode.broccoli.R;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class SearchRecipeTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Before
    public void before() throws InterruptedException {
        Thread.sleep(2000);

        onView(allOf(withId(R.id.fab_recipes), withContentDescription("New Recipe"),
                isDisplayed())).perform(click());

        onView(allOf(withId(R.id.new_title),
                isDisplayed())).perform(replaceText("Fry Rice"));
        onView(allOf(withId(R.id.new_ingredients),
                isDisplayed())).perform(replaceText("Rice"));
        onView(allOf(withId(R.id.button_save_recipe),
                isDisplayed())).perform(click());
        onView(allOf(withContentDescription("Navigate up"),
                isDisplayed())).perform(click());

        Thread.sleep(1000);
        onView(allOf(withId(R.id.fab_recipes), withContentDescription("New Recipe"),
                isDisplayed())).perform(click());

        onView(allOf(withId(R.id.new_title),
                isDisplayed())).perform(replaceText("Salad"));
        onView(allOf(withId(R.id.new_ingredients),
                isDisplayed())).perform(replaceText("lettuce"));
        onView(allOf(withId(R.id.button_save_recipe),
                isDisplayed())).perform(click());
        onView(allOf(withContentDescription("Navigate up"),
                isDisplayed())).perform(click());
    }

    @Test
    public void searchRecipeTest() throws InterruptedException {
        onView(allOf(withId(R.id.action_search), withContentDescription("Search"))).perform(click());
        Thread.sleep(1000);
        onView(allOf(withId(com.google.android.material.R.id.search_src_text), isDisplayed()))
                .perform(replaceText("Chicken Soup"));

        onView(allOf(withId(com.google.android.material.R.id.search_close_btn),
                        withContentDescription("Clear query"))).check(matches(isClickable()));

    }

}
