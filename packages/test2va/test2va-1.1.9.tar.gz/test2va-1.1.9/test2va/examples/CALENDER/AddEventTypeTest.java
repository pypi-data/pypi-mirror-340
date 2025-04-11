package test2va;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.isNotClickable;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.CoreMatchers.allOf;
import static org.hamcrest.CoreMatchers.anyOf;
import static org.hamcrest.CoreMatchers.containsString;

import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import org.fossify.calendar.R;
import org.fossify.calendar.activities.MainActivity;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class AddEventTypeTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
        new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void addEventTypeTest() throws InterruptedException {

        onView(allOf(withContentDescription("Settings"), withId(R.id.settings)))
            .perform(click());

        onView(withId(R.id.settings_manage_event_types_holder)).perform(click());
        onView(withId(R.id.add_event_type)).perform(click());
        onView(withId(R.id.type_title)).perform(replaceText("Family Event"));
        onView(allOf(withId(android.R.id.button1), withText("OK"))).perform(click());

        Thread.sleep(1000);
        onView(allOf(withText("Family Event"), withId(R.id.event_type_title))).check(matches(isDisplayed()));
        
    }
}
