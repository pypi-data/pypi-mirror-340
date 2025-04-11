package test2va;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isClickable;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.isEnabled;
import static androidx.test.espresso.matcher.ViewMatchers.isNotClickable;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.CoreMatchers.allOf;
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
public class UpdateToWeeklyViewTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
        new ActivityScenarioRule<>(MainActivity.class);

    @Test
    public void updateToWeeklyViewTest() throws InterruptedException {

        onView(allOf(withContentDescription("Change view"), withId(R.id.change_view)))
            .perform(click());
        onView(allOf(withText("Weekly view"), withClassName(containsString("RadioButton"))))
            .perform(click());
        Thread.sleep(1000);
        onView(withId(R.id.week_view_days_count)).check(matches(isEnabled()));
    }
}
