
# test to_dict and from_dict


import pytest
import gmft
from gmft.pdf_bindings import PyPDFium2Document


@pytest.fixture(scope="session")
def doc_tiny():
    doc = PyPDFium2Document("test/samples/tiny.pdf")
    yield doc
    # cleanup
    doc.close()
    

def test_pypdfium2_bindings(doc_tiny):
    doc = doc_tiny
    PyPDFium2Document("test/samples/tiny.pdf")
    assert len(doc) == 1
    page = doc.get_page(0) 
    #type: gmft.pdf_bindings.BasePage
    
    img = page.get_image()
    assert img.width == 612
    assert img.height == 792
    
    assert page.get_filename() == "test/samples/tiny.pdf"
    assert page.page_number == 0
    
    
    

def test_pypdfium2_image(doc_tiny):
    doc = doc_tiny
    page = doc.get_page(0) 
    #type: gmft.pdf_bindings.BasePage
    img = page.get_image()
    assert img.width == 612
    assert img.height == 792
    
    img = page.get_image(dpi=100)
    assert img.width == 850
    assert img.height == 1100
    
    img = page.get_image(dpi=72, rect=gmft.Rect((0, 0, 100, 100)))
    assert img.width == 100
    assert img.height == 100
    
    img = page.get_image(dpi=72, rect=gmft.Rect((50, 50, 100, 150)))
    assert img.width == 50
    assert img.height == 100
        

def test_pypdfium2_positions(doc_tiny):
    doc = doc_tiny
    page = doc.get_page(0) 
    #type: gmft.pdf_bindings.BasePage
    
    # get reference positions from tiny_pdfium.txt
    with open("test/samples/tiny_pdfium.tsv") as f:
        reference = f.readlines()
    
    actual = list(page.get_positions_and_text())
    
    EPS = 0.01
    for ref, pos in zip(reference, actual):
        ref_bbox, ref_text = ref.rsplit("\t", 1)
        ref_text = ref_text.strip()
        act_bbox = pos[:4]
        act_text = pos[4]
        assert ref_text == act_text, f"Different text: expected {ref_text}, got {act_text}"
        for ref, pos in zip(ref_bbox.split(), act_bbox):
            ref = float(ref)
            pos = float(pos)
            assert abs(ref - pos) < EPS, f"Different positions: expected {ref}, got {pos}"    
    
    # tuples = list(page.get_positions_and_text())
    
    # # save to test/samples/tiny_pdfium.tsv
    # with open("test/samples/tiny.tsv", "w") as f:
    #     for tup in tuples:
    #         f.write("\t".join(map(str, tup)) + "\n")
        