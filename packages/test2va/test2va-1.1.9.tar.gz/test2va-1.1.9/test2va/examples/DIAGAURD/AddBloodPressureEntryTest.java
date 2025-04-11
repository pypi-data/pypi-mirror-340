package com.faltenreich.diaguard.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.action.ViewActions.scrollTo;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.anything;
import static org.hamcrest.Matchers.is;

import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import com.faltenreich.diaguard.R;
import com.faltenreich.diaguard.feature.navigation.MainActivity;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class AddBloodPressureEntryTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Before
    public void prepare() {
        onView(withContentDescription("Open Navigator")).perform(click());
        onView(withId(R.id.nav_log)).perform(click());
    }

    @Test
    public void addBloodPressureEntryTest() throws InterruptedException {

        onView(allOf(withId(R.id.fab_primary),
                withContentDescription("New entry"))).perform(click());
        onView(allOf(withId(R.id.fab_secondary),
                withContentDescription("Add measurement"))).perform(click());
        onView(withText("Blood Pressure")).perform(click());
        onView(allOf(withId(android.R.id.button1), withText("OK")))
                .perform(scrollTo());
        onView(allOf(withId(android.R.id.button1), withText("OK")))
                .perform(click());
        Thread.sleep(2000);
        onView(allOf(withId(R.id.edit_text),
                withParent(withParent(withId(R.id.systolic_input_field))))).
                perform(replaceText("120"));
        onView(allOf(withId(R.id.edit_text),
                withParent(withParent(withId(R.id.diastolic_input_field))))).
                perform(replaceText("70"));
        onView(withId(R.id.fab_primary)).perform(click());

        onView(allOf(withId(R.id.value), withText("120 to 70 mm Hg")))
                .check(matches(isDisplayed()));
    }

}
