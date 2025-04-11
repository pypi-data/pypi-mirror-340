package org.totschnig.myexpenses.test2va;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.action.ViewActions.scrollTo;
import static androidx.test.espresso.assertion.ViewAssertions.doesNotExist;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.hasDescendant;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.isNotChecked;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.containsStringIgnoringCase;

import androidx.test.ext.junit.rules.ActivityScenarioRule;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.totschnig.myexpenses.R;
import org.totschnig.myexpenses.activity.SplashActivity;

public class DeleteTransactionTest {

    @Rule
    public ActivityScenarioRule<SplashActivity> rule = new ActivityScenarioRule<>(SplashActivity.class);

    @Before
    public void setup() throws InterruptedException {
        //OnboardingActivity
        onView(allOf(withText("Next"),
                isDisplayed())).perform(click());
        onView(allOf(withText("Next"),
                isDisplayed())).perform(click());
        onView(allOf(withText("Get started"),
                isDisplayed())).perform(click());

        // add first expense
        onView(allOf(withId(R.id.fab),
                isDisplayed())).perform(click());
        Thread.sleep(1000);
        onView(allOf(withId(R.id.AmountEditText), withParent(allOf(withId(R.id.Amount),
                hasDescendant(allOf(withId(R.id.TaType), isNotChecked())))))).perform(replaceText("50"));
        onView(allOf(withId(R.id.fab), isDisplayed())).perform(click());

        // add second expense
        onView(allOf(withId(R.id.fab),
                isDisplayed())).perform(click());
        Thread.sleep(1000);
        onView(allOf(withId(R.id.AmountEditText), withParent(allOf(withId(R.id.Amount),
                hasDescendant(allOf(withId(R.id.TaType), isNotChecked())))))).perform(replaceText("30"));
        onView(allOf(withId(R.id.fab), isDisplayed())).perform(click());

    }

    @Test
    public void deleteTransactionTest() throws InterruptedException {

        onView(withText("-$30.00")).perform(click());
        onView(withText("Delete")).perform(click());
        onView(allOf(withText("Delete"),withId(android.R.id.button1))).perform(click());

        Thread.sleep(1000);
        onView(withText(containsStringIgnoringCase("-$30.00"))).check(doesNotExist());
    }
}
