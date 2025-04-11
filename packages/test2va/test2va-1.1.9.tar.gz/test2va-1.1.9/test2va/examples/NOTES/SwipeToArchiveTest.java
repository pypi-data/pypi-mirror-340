package com.maltaisn.notes.test2va;


import static androidx.test.espresso.Espresso.onView;
import static androidx.test.espresso.Espresso.pressBack;
import static androidx.test.espresso.action.ViewActions.click;
import static androidx.test.espresso.action.ViewActions.closeSoftKeyboard;
import static androidx.test.espresso.action.ViewActions.replaceText;
import static androidx.test.espresso.action.ViewActions.swipeLeft;
import static androidx.test.espresso.action.ViewActions.typeText;
import static androidx.test.espresso.assertion.ViewAssertions.matches;
import static androidx.test.espresso.contrib.RecyclerViewActions.actionOnItemAtPosition;
import static androidx.test.espresso.matcher.ViewMatchers.isDisplayed;
import static androidx.test.espresso.matcher.ViewMatchers.withClassName;
import static androidx.test.espresso.matcher.ViewMatchers.withContentDescription;
import static androidx.test.espresso.matcher.ViewMatchers.withId;
import static androidx.test.espresso.matcher.ViewMatchers.withParent;
import static androidx.test.espresso.matcher.ViewMatchers.withText;
import static org.hamcrest.Matchers.allOf;
import static org.hamcrest.Matchers.containsString;
import static org.hamcrest.Matchers.is;

import android.view.View;
import android.view.ViewGroup;
import android.view.ViewParent;

import androidx.test.espresso.ViewInteraction;
import androidx.test.ext.junit.rules.ActivityScenarioRule;
import androidx.test.ext.junit.runners.AndroidJUnit4;
import androidx.test.filters.LargeTest;

import com.maltaisn.notes.R;
import com.maltaisn.notes.ui.main.MainActivity;

import org.hamcrest.Description;
import org.hamcrest.Matcher;
import org.hamcrest.TypeSafeMatcher;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;

@LargeTest
@RunWith(AndroidJUnit4.class)
public class SwipeToArchiveTest {

    @Rule
    public ActivityScenarioRule<MainActivity> mActivityScenarioRule =
            new ActivityScenarioRule<>(MainActivity.class);

    @Before
    public void before() throws InterruptedException {
        onView(allOf(withId(R.id.fab), withContentDescription("Create note"))).perform(click());
        onView(allOf(withId(R.id.title_edt), withClassName(containsString("EditText")))).perform(typeText("Note1"));
        pressBack();
        pressBack();
        Thread.sleep(1000);

        onView(allOf(withId(R.id.fab), withContentDescription("Create note"))).perform(click());
        onView(allOf(withId(R.id.title_edt), withClassName(containsString("EditText")))).perform(typeText("Note2"));
        pressBack();
        pressBack();
        Thread.sleep(1000);

    }

    @Test
    public void swipeToArchiveTest() {

        onView(allOf(withId(R.id.title_txv), withText(containsString("Note1")))).perform(swipeLeft());
        onView(withText("Undo")).check(matches(isDisplayed()));
    }

}
