import unittest
import pandas as pd

from fitbit_reader import fitbit_steps_tools as tools


class TestFitbitStepsTools(unittest.TestCase):

    def test_split_into_single_dataframe(self):
        dataframe_ = pd.DataFrame({
            "Steps":
                [40, 42, 40, 20, 0, 45, 42, 0, 0, 0, 50, 50, 52],
            "DataColumn2":
                [40, 42, 40, 20, 0, 45, 42, 0, 0, 0, 50, 50, 52],
        })
        dfs = tools.get_active_steps_dataframes(
            dataframe_,
            min_steps_for_entry_to_be_active=40,
            max_contiguous_non_active_entries_for_continuous_session=2,
            min_consecutive_active_entries_to_count_as_activity=5,
        )
        self.assertEqual(1, len(dfs))
        true_df1 = [40, 42, 40, 45, 42]
        test_df1 = list(dfs[0].Steps)
        test_df1_sub_col = list(dfs[0].DataColumn2)
        for i in range(len(true_df1)):
            self.assertEqual(
                true_df1[i],
                test_df1[i]
            )
            self.assertEqual(
                true_df1[i],
                test_df1_sub_col[i]
            )

        dfs = tools.get_active_steps_dataframes(
            dataframe_,
            min_steps_for_entry_to_be_active=40,
            max_contiguous_non_active_entries_for_continuous_session=3,
            min_consecutive_active_entries_to_count_as_activity=5,
        )
        self.assertEqual(1, len(dfs))
        true_df1 = [40, 42, 40, 45, 42, 50, 50, 52]
        test_df1 = list(dfs[0].Steps)
        test_df1_sub_col = list(dfs[0].DataColumn2)
        for i in range(len(true_df1)):
            self.assertEqual(
                true_df1[i],
                test_df1[i]
            )
            self.assertEqual(
                true_df1[i],
                test_df1_sub_col[i]
            )

    def test_split_into_multiple_dataframes(self):
        dataframe_ = pd.DataFrame({
            "Steps":
                [40, 42, 40, 20, 0, 45, 42, 0, 0, 0, 50, 50, 52],
        })

        dfs = tools.get_active_steps_dataframes(
            dataframe_,
            min_steps_for_entry_to_be_active=40,
            max_contiguous_non_active_entries_for_continuous_session=1,
            min_consecutive_active_entries_to_count_as_activity=2,
        )
        self.assertEqual(3, len(dfs))
        true_dfs = [
            [40, 42, 40],
            [45, 42],
            [50, 50, 52]
        ]
        test_dfs = [
            list(dfs[0].Steps),
            list(dfs[1].Steps),
            list(dfs[2].Steps)
        ]
        for j in range(len(true_dfs)):
            for i in range(len(true_dfs[j])):
                self.assertEqual(
                    true_dfs[j][i],
                    test_dfs[j][i]
                )

    def test_get_active_steps(self):
        dataframe_ = pd.DataFrame({
            "Steps":
                [40, 40, 40, 20, 0, 40, 40, 0, 0, 0, 50, 50, 50],
        })

        self.assertEqual(
            370,
            tools.get_total_active_steps(
                dataframe_,
                min_steps_for_entry_to_be_active=0,
                max_contiguous_non_active_entries_for_continuous_session=0,
                min_consecutive_active_entries_to_count_as_activity=0,
            )
        )

        self.assertEqual(
            290,
            tools.get_total_active_steps(
                dataframe_,
                min_steps_for_entry_to_be_active=1,
                max_contiguous_non_active_entries_for_continuous_session=0,
                min_consecutive_active_entries_to_count_as_activity=3,
            )
        )

        self.assertEqual(
            200,
            tools.get_total_active_steps(
                dataframe_,
                min_steps_for_entry_to_be_active=40,
                max_contiguous_non_active_entries_for_continuous_session=2,
                min_consecutive_active_entries_to_count_as_activity=5,
            )
        )

        self.assertEqual(
            150,
            tools.get_total_active_steps(
                dataframe_,
                min_steps_for_entry_to_be_active=45,
                max_contiguous_non_active_entries_for_continuous_session=2,
                min_consecutive_active_entries_to_count_as_activity=3,
            )
        )

    def test_no_active_steps(self):
        dataframe_ = pd.DataFrame({
            "Steps":
                [40, 40, 40, 20, 0, 40, 40, 0, 0, 0, 50, 50, 50],
        })

        self.assertEqual(
            None,
            tools.get_active_steps_dataframe(
                dataframe_,
                min_steps_for_entry_to_be_active=200,
                max_contiguous_non_active_entries_for_continuous_session=0,
                min_consecutive_active_entries_to_count_as_activity=0,
            )
        )

        self.assertEqual(
            0,
            tools.get_total_active_steps(
                dataframe_,
                min_steps_for_entry_to_be_active=200,
                max_contiguous_non_active_entries_for_continuous_session=0,
                min_consecutive_active_entries_to_count_as_activity=0,
            )
        )
