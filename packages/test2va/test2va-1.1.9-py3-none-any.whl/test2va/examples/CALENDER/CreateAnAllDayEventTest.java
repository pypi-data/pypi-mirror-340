package test2va;

import static androidx.test.espresso.Espresso.closeSoftKeyboard;
import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.hasDescendant;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.isEnabled;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withParentIndex;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.CoreMatchers.allOf;
import static org.hamcrest.CoreMatchers.anyOf;
import static org.hamcrest.CoreMatchers.containsString;

import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import org.fossify.calendar.R;
import org.fossify.calendar.activities.MainActivity;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class CreateAnAllDayEventTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
        new ActivityScenarioRule<>(MainActivity.class);

    @Before
    public void prepareTest() throws InterruptedException {
        onView(allOf(withContentDescription("Change view"), withId(R.id.change_view)))
            .perform(click());
        onView(allOf(withText("Simple event list"), withClassName(containsString("RadioButton"))))
            .perform(click());

        onView(allOf(withId(R.id.calendar_fab), withContentDescription("New Event"))).perform(click());
        onView(allOf(withText("Event"))).perform(click());
        onView(allOf(withId(R.id.event_title), withClassName(containsString("EditText"))))
            .perform(replaceText("Event1"));
        onView(allOf(withId(R.id.save), withContentDescription("Save")))
            .perform(click());
        Thread.sleep(1000);
        onView(allOf(withText("OK"), withId(android.R.id.button1))).perform(click());
    }

    @Test
    public void createAnAllDayEventTest() throws InterruptedException {
        Thread.sleep(5000);

        onView(allOf(withId(R.id.calendar_fab), withContentDescription("New Event"))).perform(click());
        onView(allOf(withId(R.id.fab_event_label), withText("Event"))).perform(click());
        closeSoftKeyboard();

        // enter title
        onView(allOf(withId(R.id.event_title), withClassName(containsString("EditText"))))
            .perform(replaceText("Workshop"));
        // check all day
        onView(allOf(withId(R.id.event_all_day), withText("All-day"))).perform(click());
        onView(allOf(withId(R.id.save), withContentDescription("Save")))
            .perform(click());
        Thread.sleep(1000);

        onView(allOf(withId(R.id.event_item_title), withText("Workshop"), withParent(hasDescendant(withText("All-day")))))
            .check(matches(isDisplayed()));

    }
}
