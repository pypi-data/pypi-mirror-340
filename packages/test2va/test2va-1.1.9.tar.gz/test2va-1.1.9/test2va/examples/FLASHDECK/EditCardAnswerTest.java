package m.co.rh.id.a_flash_deck.app.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.assertion.ViewAssertions.doesNotExist;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.hasDescendant;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withParentIndex;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsStringIgnoringCase;

import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import m.co.rh.id.a_flash_deck.R;
import m.co.rh.id.a_flash_deck.app.MainActivity;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class EditCardAnswerTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Before
    public void before() throws InterruptedException {
        Thread.sleep(2000);

        onView(allOf(withId(R.id.button_add_deck))).perform(click());
        onView(withId(R.id.edit_text_name)).perform(replaceText("Keto Fruit"));
        onView(allOf(withId(R.id.button_save))).perform(click());
        Thread.sleep(1000);

        onView(allOf(withId(R.id.button_add_deck))).perform(click());
        onView(withId(R.id.edit_text_name)).perform(replaceText("Diet Meal"));
        onView(allOf(withId(R.id.button_save))).perform(click());
        Thread.sleep(1000);

        onView(allOf(withId(R.id.button_add_card))).perform(click());
        Thread.sleep(2000);
        onView(allOf(withId(R.id.text_deck_name))).perform(click());
        Thread.sleep(2000);
        onView(allOf(withId(R.id.button_ok))).perform(click());

        onView(allOf(withId(R.id.text_input_edit_question)))
                .perform(replaceText("Bananas"));
        onView(allOf(withId(R.id.text_input_edit_answer)))
                .perform(replaceText("No"));
        Thread.sleep(2000);

        onView(allOf(withId(R.id.menu_save), withContentDescription("Save"))).perform(click());
        Thread.sleep(2000);

        onView(allOf(withId(R.id.button_add_card))).perform(click());
        Thread.sleep(2000);
        onView(allOf(withId(R.id.text_deck_name), withText("Keto Fruit"))).perform(click());
        Thread.sleep(2000);
        onView(allOf(withId(R.id.button_ok))).perform(click());

        onView(allOf(withId(R.id.text_input_edit_question)))
                .perform(replaceText("Blueberry"));
        onView(allOf(withId(R.id.text_input_edit_answer)))
                .perform(replaceText("No"));
        Thread.sleep(2000);

        onView(allOf(withId(R.id.menu_save), withContentDescription("Save"))).perform(click());
        Thread.sleep(2000);

    }
    @Test
    public void editCardAnswerTest() throws InterruptedException {
        onView(withClassName(containsStringIgnoringCase("ImageButton"))).perform(click());
        Thread.sleep(2000);
        onView(allOf(withId(R.id.menu_cards), withText("Cards"))).perform(click());
        Thread.sleep(2000);

        onView(allOf(withId(R.id.button_edit),
                withParent(withParent(hasDescendant(withText(containsStringIgnoringCase("Blueberry"))))))).perform(click());

        onView(withId(R.id.text_input_edit_answer)).perform(replaceText("Yes"));
        onView(allOf(withId(R.id.menu_save), withContentDescription("Save"))).perform(click());
        Thread.sleep(2000);

        onView(allOf(withId(R.id.text_answer), withText("A: Yes"), withParent(hasDescendant(withText("Q: Blueberry")))))
                .check(matches(isDisplayed()));

    }

}
