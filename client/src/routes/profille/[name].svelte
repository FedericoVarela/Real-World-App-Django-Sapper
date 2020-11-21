<!-- <script context="module" lang="ts">
    import { get } from "../../api";
    import { match } from "../../utils";
    import type { Post } from "../../types";
  
    export async function preload({ params }, _) {
      const { name } = params;
  
      const res = await get<Post>(`posts/${id}`);
      return match(
        res,
        (data: Post) => {
          return { data };
        },
        (_: Error) => {
          this.error(404, "Not found");
        }
      );
    }
  </script> -->