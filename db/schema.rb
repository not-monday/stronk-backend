# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 26) do

  create_table "exercise_tracking", id: false, force: :cascade do |t|
    t.integer "user_id"
    t.integer "exercise_id"
    t.date "date"
    t.integer "weight"
    t.integer "reps"
  end

  create_table "exercises", force: :cascade do |t|
    t.string "description"
    t.string "name"
  end

  create_table "program_reviews", force: :cascade do |t|
    t.integer "program_id"
    t.string "author"
    t.integer "rating"
    t.string "review"
  end

  create_table "program_workout", id: false, force: :cascade do |t|
    t.integer "program_id"
    t.integer "workout_id"
  end

  create_table "programs", force: :cascade do |t|
    t.integer "author"
    t.integer "duration"
    t.string "description"
    t.string "name"
  end

  create_table "users", force: :cascade do |t|
    t.string "username"
    t.string "password"
    t.string "email"
    t.string "current_program"
    t.string "name"
  end

  create_table "weights", force: :cascade do |t|
    t.date "date"
    t.integer "weight"
    t.integer "user_id"
    t.string "name"
  end

  create_table "workout_exercise", id: false, force: :cascade do |t|
    t.integer "workout_id"
    t.integer "exercise_id"
  end

  create_table "workouts", force: :cascade do |t|
    t.string "description"
    t.integer "projected_time"
    t.string "name"
  end

end
