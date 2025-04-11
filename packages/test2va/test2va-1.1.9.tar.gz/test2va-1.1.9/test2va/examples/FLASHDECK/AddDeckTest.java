package m.co.rh.id.a_flash_deck.app.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.closeSoftKeyboard;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.action.ViewActions.scrollTo;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsStringIgnoringCase;
import static org.hamcrest.Matchers.is;

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
public class AddDeckTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Before
    public void before() throws InterruptedException {
        Thread.sleep(2000);
    }


    @Test
    public void addDeckTest() throws InterruptedException {
        onView(allOf(withId(R.id.button_add_deck), withText("Add Deck"))).perform(click());

        onView(withId(R.id.edit_text_name)).perform(replaceText("Keto Fruit"));
        closeSoftKeyboard();

        onView(allOf(withId(R.id.button_save))).perform(click());
        Thread.sleep(2000);
        onView(withClassName(containsStringIgnoringCase("ImageButton"))).perform(click());
        Thread.sleep(2000);
        onView(allOf(withId(R.id.menu_decks), withText("Decks"))).perform(click());
        Thread.sleep(2000);


        onView(allOf(withId(R.id.text_deck_name), withText("Keto Fruit"))).check(matches(isDisplayed()));
        onView(allOf(withText("Deck List"), withParent(withId(R.id.toolbar)))).check(matches(isDisplayed()));
    }

}
