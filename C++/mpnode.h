#pragma once

typedef enum {
	// 系数
	COEF,
	// 广义表
	LIST
} ElemTag;

class MPList;

struct MPNode {
	// COEF 表示系数，LIST 表示表节点
	ElemTag elem_tag;

	// 指数域
	int exp;

	union
	{
		// 系数
		float coef;
		// 广义表指针
		MPList* list_ptr;
	};
	// 指向下一个节点的指针
	MPNode* tp;
	// 两个节点相乘
	friend MPNode operator *(const MPNode&, const MPNode&);
	// 节点和数相乘
	friend MPNode operator *(const MPNode&, float);
	friend MPNode operator *(float, const MPNode&);
	// 当前节点与另一个节点相加后赋值给自身
	MPNode* operator +=(const MPNode&);
};
