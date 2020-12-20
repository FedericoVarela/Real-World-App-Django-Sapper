import type { Comment } from "./types"


export class Node {
    data: Comment
    children: Node[]

    constructor(data: Comment, children: Node[]) {
        this.data = data;
        this.children = children;
    }
}

function createNodeMap(comments: Comment[]): Map<number, Node> {
    const res = new Map();
    for (let cmt of comments) {
        res.set(cmt.id, new Node(cmt, []));
    }
    return res
}


export class CommentTree {
    roots: Node[];

    constructor(comments: Comment[]) {
        const nodeMap = createNodeMap(comments)
        this.roots = []
        // The map is already ordered by ID in reverse
        nodeMap.forEach(node => {
            if (node.data.reply_to !== null) {
                // The parent comment may not be loaded yet because of pagination
                // If that's the case, then the comment is not considered
                const nodeIfExists = nodeMap.get(node.data.reply_to)
                if (nodeIfExists !== undefined) {
                    nodeMap.get(node.data.reply_to).children.push(node);
                }
            } else {
                this.roots.push(node)
            }
        })
    }
}