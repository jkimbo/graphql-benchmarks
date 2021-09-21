import http from "k6/http";
import { check } from "k6";

export let options = {
  stages: [
    {
      duration: "15s",
      target: 1
    }
  ]
};

export default function() {
  const payload = JSON.stringify({
    query: `query {
      top250 {
        id
        imdbId
        title
        year
        imageUrl
        imdbRating
        imdbRatingCount
        director {
          id
          name
        }
      }
    }
    `
  });
  const params = {
    headers: {
      "Content-Type": "application/json"
    }
  };
  const url = "http://localhost:8000";
  const response = http.post(`${url}/graphql/`, payload, params);

  check(response, {
    "is status 200": r => r.status === 200
  });
  check(response, {
    "is response correct": r => {
      return (
        response.json().data.top250.length === 250 &&
        response.json().data.top250[0].title === "The Shawshank Redemption"
      );
    }
  });
}
