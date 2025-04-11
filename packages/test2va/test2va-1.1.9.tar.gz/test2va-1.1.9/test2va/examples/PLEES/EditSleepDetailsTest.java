package hu.vmiklos.plees_tracker.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withParentIndex;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;

import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

import hu.vmiklos.plees_tracker.MainActivity;
import hu.vmiklos.plees_tracker.R;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class EditSleepDetailsTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Before
    public void before() throws InterruptedException {
        Thread.sleep(2000);

        onView(allOf(withId(R.id.start_stop_text), withText("Start"))).perform(click());
        Thread.sleep(2000);
        onView(allOf(withId(R.id.start_stop_text), withText("Stop"))).perform(click());

        onView(allOf(withId(R.id.start_stop_text), withText("Start"))).perform(click());
        Thread.sleep(2000);
        onView(allOf(withId(R.id.start_stop_text), withText("Stop"))).perform(click());

    }

    @Test
    public void editSleepDetailsTest() throws InterruptedException {
        Thread.sleep(1000);
        onView(allOf(withId(R.id.sleep_swipeable), withParent(withParentIndex(0)))).perform(click());

        // edit start time
        onView(withId(R.id.sleep_start_time)).perform(click());
        onView(withContentDescription("1")).perform(click());
        onView(withContentDescription("0")).perform(click());
        onView(withText("PM")).perform(click());
        onView(allOf(withText("OK"), withId(android.R.id.button1))).perform(click());

        // edit end time
        onView(withId(R.id.sleep_stop_time)).perform(click());
        onView(withContentDescription("1")).perform(click());
        onView(withContentDescription("30")).perform(click());
        onView(withText("PM")).perform(click());
        onView(allOf(withText("OK"), withId(android.R.id.button1))).perform(click());

        onView(allOf(withText("13:00"), withId(R.id.sleep_start_time))).check(matches(isDisplayed()));
        onView(allOf(withText("13:30"), withId(R.id.sleep_stop_time))).check(matches(isDisplayed()));
    }


}
