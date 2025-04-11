package com.flauschcode.broccoli.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.assertion.ViewAssertions.doesNotExist;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;

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
public class EditRecipeIngredientsTest {

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
    public void editRecipeIngredientsTest() throws InterruptedException {
        onView(allOf(withId(R.id.card_text_view_title), withText("Salad"))).perform(click());
        onView(withContentDescription("More options")).perform(click());
        Thread.sleep(1000);
        onView(withText("Edit")).perform(click());
        onView(allOf(withId(R.id.new_ingredients),
                isDisplayed())).perform(replaceText("Egg, Lettuce, Potato"));
        onView(withId(R.id.button_save_recipe)).perform(click());

        onView(allOf(withText("Egg, Lettuce, Potato"), withId(R.id.ingredient_text)))
                .check(matches(isDisplayed()));

    }
    
}
