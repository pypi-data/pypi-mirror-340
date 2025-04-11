package org.totschnig.myexpenses.test2va;

import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.action.ViewActions.scrollTo;
import static androidx.test.espresso.action.ViewActions.typeText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.hasDescendant;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.isNotChecked;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withParentIndex;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsString;

import androidx.test.ext.junit.rules.ActivityScenarioRule;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.totschnig.myexpenses.R;
import org.totschnig.myexpenses.activity.SplashActivity;

public class SortingByAmountTest {

    @Rule
    public ActivityScenarioRule<SplashActivity> rule = new ActivityScenarioRule<>(SplashActivity.class);

    @Before
    public void setup() {
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
        Thread.sleep(2000);
        onView(allOf(withId(R.id.AmountEditText), withParent(allOf(withId(R.id.Amount),
                hasDescendant(allOf(withId(R.id.TaType), isNotChecked())))))).perform(replaceText("50"));
        onView(allOf(withId(R.id.Comment),
                isDisplayed())).perform(typeText("Grocery"));
        onView(allOf(withId(R.id.fab),
                isDisplayed())).perform(click());

        // add second expense
        onView(allOf(withId(R.id.fab),
                isDisplayed())).perform(click());
        Thread.sleep(2000);
        onView(allOf(withId(R.id.AmountEditText), withParent(allOf(withId(R.id.Amount),
                hasDescendant(allOf(withId(R.id.TaType), isNotChecked())))))).perform(replaceText("30"));
        onView(allOf(withId(R.id.Comment),
                isDisplayed())).perform(typeText("Movie"));
        onView(allOf(withId(R.id.fab),
                isDisplayed())).perform(click());
    }

    @Test
    public void sortingByAmountTest() throws InterruptedException {

        onView(withContentDescription(containsString("More options"))).perform(click());
        Thread.sleep(2000);
        onView(withText("Sort by")).perform(click());
        Thread.sleep(2000);
        onView(withText("Amount / Descending")).perform(click());
        Thread.sleep(2000);


        onView(allOf(withText(containsString("-$50.00")), withParent(withParentIndex(0))))
                .check(matches(isDisplayed()));
        onView(allOf(withText(containsString("-$30.00")), withParent(withParentIndex(1))))
                .check(matches(isDisplayed()));

    }
}
