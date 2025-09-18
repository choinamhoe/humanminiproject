const SERVER_URL =
  process.env.NODE_ENV === "production" ? "/node" : "http://localhost:8000";

const URL = {
  HOME: "/",
  SERVER_URL,
  TEST_PATH: "/test",
};
export default URL;
