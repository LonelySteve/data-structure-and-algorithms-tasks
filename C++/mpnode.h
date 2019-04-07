#pragma once

typedef enum {
	// ϵ��
	COEF,
	// �����
	LIST
} ElemTag;

class MPList;

struct MPNode {
	// COEF ��ʾϵ����LIST ��ʾ��ڵ�
	ElemTag elem_tag;

	// ָ����
	int exp;

	union
	{
		// ϵ��
		float coef;
		// �����ָ��
		MPList* list_ptr;
	};
	// ָ����һ���ڵ��ָ��
	MPNode* tp;
	// �����ڵ����
	friend MPNode operator *(const MPNode&, const MPNode&);
	// �ڵ�������
	friend MPNode operator *(const MPNode&, float);
	friend MPNode operator *(float, const MPNode&);
	// ��ǰ�ڵ�����һ���ڵ���Ӻ�ֵ������
	MPNode* operator +=(const MPNode&);
};
