#
# Copyright 2022 Deephaven Data Labs
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# https://gist.github.com/devinrsmith/86cc76be15167322b0d003271255a806

from deephaven import csv, parquet

csv_path = '2022_place_canvas_history.csv'
parquet_path = '2022_place_deephaven.parquet'
compression_codec_name = 'ZSTD'

# 1. Read the place canvas history CSV
place_raw = csv.read(csv_path)

# 2. Cleanup the data
# a. use an increasing numeric id for user_id instead of a large string
user_ids = place_raw.select_distinct("user_id").update_view("K=k")
# b. translate the hex pixel_color to an int rgb column
# c. break out coordinate to x1, y1, x2, and y2 columns
# d. sort by timestamp (raw data is not sorted) 
place = place_raw\
    .exact_join(user_ids, "user_id", "K")\
    .update_view([
        "rgb=Integer.parseInt(pixel_color.substring(1), 16)",
        "coordinates=coordinate.split(`,`)",
        "x1=Short.parseShort(coordinates[0])",
        "y1=Short.parseShort(coordinates[1])",
        "x2=coordinates.length == 2 ? NULL_SHORT : Short.parseShort(coordinates[2])",
        "y2=coordinates.length == 2 ? NULL_SHORT : Short.parseShort(coordinates[3])"])\
    .view(["timestamp", "user_id=(int)K", "rgb", "x1", "y1", "x2", "y2"])\
    .sort("timestamp")

# 3. Write to a Parquet file with ZSTD compression and share with others! 
parquet.write(place, parquet_path,  compression_codec_name=compression_codec_name)